import os

from quart import Quart, abort, jsonify, request

from alttprbot.alttprgen.mystery import get_weights, generate_random_settings
from alttprbot.database import sgl2020_tournament, config
from alttprbot_discord.bot import discordbot
from alttprbot_srl import nick_verifier
from alttprbot_srl.bot import srlbot

sahasrahbotapi = Quart(__name__)


@sahasrahbotapi.route('/srl/verification/<string:nick>/<int:key>', methods=['GET'])
async def verify_srl_user(nick, key):
    result = await nick_verifier.verify_nick(nick, key)
    if result:
        user = discordbot.get_user(result['discord_user_id'])
        await user.send("We have successfully verified your SRL nick!")
        return "We have successfully verified your SRL nick!"
    else:
        return "Unable to verify your SRL nick.  Please request another key and try again.  Contact Synack if this persists."


@sahasrahbotapi.route('/api/settingsgen/mystery', methods=['POST'])
async def mysterygen():
    weights = await request.get_json()
    settings, customizer = await generate_random_settings(weights=weights, spoilers="mystery")
    return jsonify(
        settings=settings,
        customizer=customizer,
        endpoint='/api/customizer' if customizer else '/api/randomizer'
    )


@sahasrahbotapi.route('/api/settingsgen/mystery/<string:weightset>', methods=['GET'])
async def mysterygenwithweights(weightset):
    weights = await get_weights(weightset)
    settings, customizer = await generate_random_settings(weights=weights, spoilers="mystery")
    return jsonify(
        settings=settings,
        customizer=customizer,
        endpoint='/api/customizer' if customizer else '/api/randomizer'
    )

@sahasrahbotapi.route('/api/sgl/episodes', methods=['GET'])
async def sgl_episodes():
    secret = request.args.get("secret")
    if not secret == os.environ.get('SGL_DATA_ENDPOINT_SECRET'):
        abort(401, description="secret required")

    result = await sgl2020_tournament.get_all_tournament_races()
    return jsonify(results=result)

@sahasrahbotapi.route('/api/sgl/episode/<int:episode>', methods=['GET'])
async def sgl_episode(episode):
    secret = request.args.get("secret")
    if not secret == os.environ.get('SGL_DATA_ENDPOINT_SECRET'):
        abort(401, description="secret required")

    result = await sgl2020_tournament.get_tournament_race_by_episodeid(episode)
    return jsonify(result=result)

@sahasrahbotapi.route('/api/sgl/message', methods=['POST'])
async def sgl_message():
    secret = request.args.get("secret")

    if not secret == os.environ.get('SGL_DATA_ENDPOINT_SECRET'):
        abort(401, description="secret required")

    payload = await request.get_json()

    guild_id = await config.get(0, 'SpeedGamingLiveGuild')
    guild = discordbot.get_guild(int(guild_id))

    member = guild.get_member_named(payload['discordTag'])

    if member is None:
        abort(404, description=f"{payload['discordTag']} user not found.")

    await member.send(payload['message'])

    return jsonify(success=True)

@sahasrahbotapi.route('/healthcheck', methods=['GET'])
async def healthcheck():
    if discordbot.is_closed():
        abort(500, description='Connection to Discord is closed.')

    appinfo = await discordbot.application_info()
    await discordbot.fetch_user(appinfo.owner.id)

    if not srlbot.connected:
        abort(500, description="Connection to SRL id closed.")

    info = await srlbot.whois(os.environ['SRL_NICK'])
    if not info['identified']:
        abort(500, description="SRL bot is not identified with Nickserv.")

    return jsonify(
        success=True
    )


@sahasrahbotapi.route('/robots.txt', methods=['GET'])
async def robots():
    return 'User-agent: *\nDisallow: /\n'

# @sahasrahbotapi.errorhandler(400)
# def bad_request(e):
#     return jsonify(success=False, error=repr(e))

# @sahasrahbotapi.errorhandler(404)
# def not_found(e):
#     return jsonify(success=False, error=repr(e))

# @sahasrahbotapi.errorhandler(500)
# def something_bad_happened(e):
#     return jsonify(success=False, error=repr(e))
