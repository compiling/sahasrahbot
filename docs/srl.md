---
layout: default
title:  SRL Commands
---
* Table of contents
{:toc}
# SahasrahBot SRL Commands
## $preset/$race/$quickswaprace
Use this command in the SRL race room.

This allows you to generate a game using a pre-defined combination of settings.

Example: `$preset open`

If `$quickswaprace` is the command, the item quickswap feature is enabled for the race.  Quickswap is always available for entrance randomizer races.

Here is a [list of currently supported presets](presets.md).  The preset name will be the name of the file without the .yaml extension.

You can append `--hints` to the command to enable hints.  All presets have hints disabled by default, with a few exceptions (see preset for details).

The option `--accessible` may be appended to mark the race as using an accessible ruleset.  See <https://link.alttpr.com/accessible> for details on this ruleset.

Supported for both alttphacks and smz3 games.  For smz3, only the normal and hard presets are supported.


## $mystery

Use this command in an SRL race room.

Here is a [list of currently supported weights](mystery.md).  The weightset name will be the name of the file without the .yaml extension.

Example: `$mystery weighted`

The option `--accessible` may be appended to mark the race as using an accessible ruleset.  See <https://link.alttpr.com/accessible> for details on this ruleset.

Only supported for alttphacks

## $spoiler

Use this command in the SRL race room.

This allows you to generate a spoiler race game using a pre-defined combination of settings.

Here is a [list of currently supported presets](presets.md).  The preset name will be the name of the file without the .yaml extension.

Example: `$spoiler open`

The option `--accessible` may be appended to mark the race as using an accessible ruleset.  See <https://link.alttpr.com/accessible> for details on this ruleset.

SahasrahBot, after the start of the race in SRL, will post the spoiler log in chat and will automatically begin counting down 900s minutes (1500s for alttpsm games) by default.  This can be overwritten with the argument `--studytime [seconds]`.

This bot will inform you when you're ready to begin racing.

Only supported for alttphacks and alttpsm.

## $cancel

Use this command in the SRL race room.

This command cancels an existing race.

Use this command in the SRL race room. Must be done before rerolling.

## $joinroom

Use this in #speedrunslive channel to force SahasrahBot to join the race room.

Example: `$joinroom #srl-abc12`

## $rules

Will post a link to the ALTTPR Racing Rules page.  This isn't context specific.

## $help

Gives you a link to this help page.