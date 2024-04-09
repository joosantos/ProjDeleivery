<template>
	<p v-if="props.beforeBracketType == 'third'" class="tournament-stage">{{ t("third") }}</p>
	<div
		:class="[
			'px-2 z-10 relative',
			props.width == 40 ? 'w-[40rem]' : '',
			props.width == 30 ? 'w-[30rem]' : '',
			props.width == 25 ? 'w-[25rem]' : '',
			props.afterBracketType.split('|')[1] == 'top'
				? 'after:block after:relative after:border-t-2 after:border-r-2 after:border-black after:left-7 after:-z-10 after:bottom-1/2'
				: '',
			props.afterBracketType.split('|')[1] == 'bot'
				? 'after:block after:relative after:border-b-2 after:border-r-2 after:border-black after:left-7 after:-z-10 after:bottom-full after:-translate-y-1/2 after:h-full'
				: '',
			props.afterBracketType == 'small|top' ? 'after:h-full' : '',
			props.afterBracketType == 'medium|top' ? 'after:h-[200%]' : '',
			props.afterBracketType == 'big|top' ? 'after:h-[500%]' : '',
			props.afterBracketType == 'large|top' ? 'after:h-[1000%]' : '',
			props.beforeBracketType == 'small'
				? 'before:block before:border-t-2 before:h-full before:border-black before:absolute before:right-5 before:-z-10 before:w-full before:top-1/2 before:-translate-y-px'
				: '',
			props.beforeBracketType == 'small0-5'
				? 'before:block before:border-t-2 before:h-full before:border-black before:absolute before:right-5 before:-z-10 before:w-full before:top-1/2 before:-translate-y-0.5'
				: '',
			props.beforeBracketType == 'third'
				? 'before:block before:border-b-2 before:border-l-2 before:h-[20rem] before:border-black before:absolute before:right-6 before:translate-x-0.5 before:-z-10 before:w-full before:-top-[17.25rem] before:-translate-y-px'
				: '',
		]">
		<!-- Number By Area -->
		<p class="absolute -top-5">
			{{
				props.tournament.matches.find((a) => a.number == props.number)?.number_by_area ==
					null ||
				props.tournament.matches.find((a) => a.number == props.number)?.number_by_area == 0
					? ""
					: "" +
					  props.tournament.matches
							.find((a) => a.number == props.number)
							.number_by_area.toString()
							.padStart(3, "0")
			}}
		</p>
		<!-- Global Area -->
		<p class="absolute -top-5 left-20">
			{{ props.tournament.matches.find((a) => a.number == props.number).global_number }}
		</p>
		<!-- Red Side -->
		<div class="tournament-athlete rounded-t-md before:bg-red-500 z-20">
			<!-- Show label if win is not "normal" -->
			<div
				v-if="
					props.tournament.matches.find((a) => a.number == props.number).winner_id !=
						null &&
					!props.tournament.matches.find((a) => a.number == props.number).normal_win &&
					props.tournament.matches.find((a) => a.number == props.number).winner_id !=
						props.tournament.matches.find((a) => a.number == props.number)
							.athlete_red_id
				"
				class="uppercase absolute left-3/4 px-2 -rotate-12 -translate-x-1/2 max-w-max min-w-max bg-red-300 z-50">
				{{
					props.tournament.matches.find((a) => a.number == props.number).abdicate_win
						? t("abdicate")
						: props.tournament.matches.find((a) => a.number == props.number).no_show_win
						? t("noShow")
						: props.tournament.matches.find((a) => a.number == props.number)
								.disqualified_win
						? t("disqualified")
						: ""
				}}
			</div>
			<!-- Padding -->
			<div class="w-20" />
			<!-- Name -->
			<p class="ml-auto">
				&nbsp;{{
					getAthleteNameTeam(
						props.tournament.matches.find((a) => a.number == props.number)?.athlete_red
					)
				}}&nbsp;
			</p>

			<!-- Points Judge 1 -->
			<p class="ml-auto border border-r-0 w-6 border-black">
				{{
					props.tournament.matches.find((a) => a.number == props.number)
						.points_red_judge1_round1 == null
						? ""
						: props.tournament.matches.find((a) => a.number == props.number)
								.points_red_judge1_round1 +
						  props.tournament.matches.find((a) => a.number == props.number)
								.points_red_judge1_round2
				}}
			</p>
			<!-- Points Central Referee -->
			<p class="border border-r-0 w-6 border-black">
				{{
					props.tournament.matches.find((a) => a.number == props.number)
						.points_red_central_referee_round1 == null
						? ""
						: props.tournament.matches.find((a) => a.number == props.number)
								.points_red_central_referee_round1 +
						  props.tournament.matches.find((a) => a.number == props.number)
								.points_red_central_referee_round2
				}}
			</p>
			<!-- Points Judge 2 -->
			<p class="border w-6 border-black">
				{{
					props.tournament.matches.find((a) => a.number == props.number)
						.points_red_judge2_round1 == null
						? ""
						: props.tournament.matches.find((a) => a.number == props.number)
								.points_red_judge2_round1 +
						  props.tournament.matches.find((a) => a.number == props.number)
								.points_red_judge2_round2
				}}
			</p>
		</div>
		<!-- Blue Side -->
		<div class="tournament-athlete rounded-b-md before:bg-blue-500 z-20">
			<!-- Show label if win is not "normal" -->
			<div
				v-if="
					props.tournament.matches.find((a) => a.number == props.number).winner_id !=
						null &&
					!props.tournament.matches.find((a) => a.number == props.number).normal_win &&
					props.tournament.matches.find((a) => a.number == props.number).winner_id !=
						props.tournament.matches.find((a) => a.number == props.number)
							.athlete_blue_id
				"
				class="uppercase absolute left-3/4 px-2 -rotate-12 -translate-x-1/2 min-w-max bg-red-300 opacity0 z-50">
				{{
					props.tournament.matches.find((a) => a.number == props.number).abdicate_win
						? t("abdicate")
						: props.tournament.matches.find((a) => a.number == props.number).no_show_win
						? t("noShow")
						: props.tournament.matches.find((a) => a.number == props.number)
								.disqualified_win
						? t("disqualified")
						: ""
				}}
			</div>
			<!-- Padding -->
			<div class="w-20" />
			<!-- Name -->
			<p class="ml-auto">
				&nbsp;{{
					getAthleteNameTeam(
						props.tournament.matches.find((a) => a.number == props.number)?.athlete_blue
					)
				}}&nbsp;
			</p>

			<!-- Points Judge 1 -->
			<p class="ml-auto border border-r-0 w-6 border-black">
				{{
					props.tournament.matches.find((a) => a.number == props.number)
						.points_blue_judge1_round1 == null
						? ""
						: props.tournament.matches.find((a) => a.number == props.number)
								.points_blue_judge1_round1 +
						  props.tournament.matches.find((a) => a.number == props.number)
								.points_blue_judge1_round2
				}}
			</p>
			<!-- Points Central Referee -->
			<p class="border border-r-0 w-6 border-black">
				{{
					props.tournament.matches.find((a) => a.number == props.number)
						.points_blue_central_referee_round1 == null
						? ""
						: props.tournament.matches.find((a) => a.number == props.number)
								.points_blue_central_referee_round1 +
						  props.tournament.matches.find((a) => a.number == props.number)
								.points_blue_central_referee_round2
				}}
			</p>
			<!-- Points Judge 3 -->
			<p class="border w-6 border-black">
				{{
					props.tournament.matches.find((a) => a.number == props.number)
						.points_blue_judge2_round1 == null
						? ""
						: props.tournament.matches.find((a) => a.number == props.number)
								.points_blue_judge2_round1 +
						  props.tournament.matches.find((a) => a.number == props.number)
								.points_blue_judge2_round2
				}}
			</p>
		</div>
	</div>
</template>

<script setup>
import { useI18n } from "vue-i18n";
import { getAthleteNameTeam as getName } from "@/services/athlete.service.js";
let { t } = useI18n();

const props = defineProps({
	tournament: {
		type: Object,
		required: true,
	},
	beforeBracketType: {
		type: String,
		required: false,
		default: "",
	},
	afterBracketType: {
		type: String,
		required: false,
		default: "none",
	},
	number: {
		type: Number,
		required: true,
	},
	width: {
		type: Number,
		required: true,
	},
});

function getAthleteNameTeam(athlete) {
	if (athlete == null) {
		return "____________________";
	}
	return getName(athlete);
}
</script>

<i18n>
{
  "en_GB": {
	  "third": "Third Place Qualification",
	  "abdicate": "Resignation",
	  "noShow": "Didn't show",
	  "disqualified": "Disqualified",
  },
  "pt_PT": {
	  "third": "Apuramento do terceiro lugar",
	  "abdicate": "Desitência",
	  "noShow": "Não compareceu",
	  "disqualified": "Desqualificado",
  }
}
</i18n>
