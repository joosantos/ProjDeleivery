<template>
	<div class="relative min-w-[100vw]min-h-[100vh]">
		<div class="xl:selection:inline-flex w-[1056px] justify-between">
			<div class="ml-4 font-bold text-3xl mt-2">
				{{ getTournamentName(props.tournament, t) }}
			</div>
			<div class="ml-4 max-w-max xl:ml-auto font-medium text-xl mt-4 xl:mt-0">
				{{
					"D" +
					(props.tournament.day == null ? "" : props.tournament.day) +
					" - A" +
					(props.tournament.area == null ? "" : props.tournament.area) +
					" - " +
					(props.tournament.morning ? t("morning") : t("afternoon"))
				}}
			</div>
		</div>
		<div class="px-4 xl:px-0">
			<div
				class="flex flex-col w-full xl:w-[48rem] xl:ml-20 mt-10 divide-y-2 divide-black rounded-lg border-2 border-black">
				<div
					v-for="(match, index) in [{}, ...props.tournament.matches]"
					:key="match.id"
					:class="[
						'flex flex-nowrap h-10',
						index == 0
							? 'rounded-t-lg font-semibold'
							: index == props.tournament.matches.length - 1 && 'rounded-b-lg',
						index == 0 ? 'bg-blue-400' : 'even:bg-blue-100 odd:bg-blue-200',
					]">
					<div class="px-2 w-10 text-center">
						<p :class="['relative top-1/2 -translate-y-1/2', index == 0 && 'text-lg']">
							{{
								index == 0
									? t("num")
									: props.tournament.matches.find((a) => a.number == index)
											?.number_by_area == null ||
									  props.tournament.matches.find((a) => a.number == index)
											?.number_by_area == 0
									? ""
									: "" +
									  props.tournament.matches
											.find((a) => a.number == index)
											.number_by_area.toString()
											.padStart(3, "0")
							}}
						</p>
					</div>
					<div class="flex-auto text-center border-black border-r-2 border-l-2">
						<p :class="['relative top-1/2 -translate-y-1/2', index == 0 && 'text-lg']">
							{{
								index == 0
									? t("athlete")
									: getAthleteNameTeam(
											props.tournament.matches.find((a) => a.number == index)
												.athlete_red
									  )
							}}
						</p>
					</div>
					<div class="px-2 w-28 text-center">
						<p v-if="index == 0" class="relative top-1/2 -translate-y-1/2 text-lg">
							{{ t("pontuation") }}
						</p>
						<div v-else class="relative w-full inline-flex mt-1.5">
							<!-- Points Judge 1 -->
							<p class="border border-r-0 w-10 border-black ml-auto">
								{{
									props.tournament.matches.find((a) => a.number == index)
										.points_red_judge1_round1 == null
										? "&nbsp;"
										: props.tournament.matches.find((a) => a.number == index)
												.points_red_judge1_round1 +
										  props.tournament.matches.find((a) => a.number == index)
												.points_red_judge1_round2
								}}
							</p>
							<!-- Points Central Referee -->
							<p class="border border-r-0 w-10 border-black">
								{{
									props.tournament.matches.find((a) => a.number == index)
										.points_red_central_referee_round1 == null
										? "&nbsp;"
										: props.tournament.matches.find((a) => a.number == index)
												.points_red_central_referee_round1 +
										  props.tournament.matches.find((a) => a.number == index)
												.points_red_central_referee_round2
								}}
							</p>
							<!-- Points Judge 2 -->
							<p class="border w-10 border-black mr-auto">
								{{
									props.tournament.matches.find((a) => a.number == index)
										.points_red_judge2_round1 == null
										? "&nbsp;"
										: props.tournament.matches.find((a) => a.number == index)
												.points_red_judge2_round1 +
										  props.tournament.matches.find((a) => a.number == index)
												.points_red_judge2_round2
								}}
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div class="h-8 sm:h-16 xl:h-40" />
		<div
			class="relative left-1/2 -translate-x-1/2 w-full xl:absolute xl:bottom-10 xl:right-20 xl:w-1/2 xl:left-auto xl:translate-x-0 xl:top-auto">
			<Judges
				:judge1="props.tournament.judge1"
				:judge2="props.tournament.judge2"
				:central="props.tournament.central_referee" />
		</div>
		<div
			class="relative left-1/2 -translate-x-1/2 max-w-min xl:absolute xl:top-16 xl:right-20 xl:left-auto xl:translate-x-0">
			<Podium :tournament="props.tournament" />
		</div>
	</div>
</template>

<script setup>
import Judges from "@/components/partials/skeletons/judges.vue";
import Podium from "@/components/partials/skeletons/podium.vue";
import { getTournamentName } from "@/services/competition.service.js";
import { getAthleteNameTeam as getName } from "@/services/athlete.service.js";
import { useI18n } from "vue-i18n";

let { t } = useI18n();

const props = defineProps({
	tournament: {
		type: Object,
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
		"num": "Nº.",
		"athlete": "Athlete Name",
		"pontuation": "Pontuation",
		"open": "Open",
		"masc": "Masculine",
		"fem": "Feminine",
		"year": "{count} Year | {count} Years",
		"final": "Final",
		"belts": {
			"white": "White",
			"white-yellow": "White and Yellow",
			"yellow": "Yellow",
			"yellow-orange": "Yellow and Orange",
			"orange": "Orange",
			"orange-purple": "Orange and Purple",
			"purple": "Purple",
			"purple-blue": "Purple and Blue",
			"blue": "Blue",
			"blue-green": "Blue and Green",
			"green": "Green",
			"brown-jr": "Brown Junior",
			"brown": "Brown",
			"black-jr": "Black Junior",
			"black": "Black",
			"duan-1": "Duan 1",
			"duan-2": "Duan 2",
			"duan-3": "Duan 3+",
		},
	},
	"pt_PT": {
		"open": "Aberto",
		"masc": "Masculino",
		"fem": "Feminino",
		"continue": "Continuar",
		"year": "{count} Ano | {count} Anos",
		"final": "Final",
		"belts": {
			"white": "Branco",
			"white-yellow": "Branco e Amarelo",
			"yellow": "Amarelo",
			"yellow-orange": "Amarelo e Laranja",
			"orange": "Laranja",
			"orange-purple": "Laranja e Púrpura",
			"purple": "Púrpura",
			"purple-blue": "Púrpura e Azul",
			"blue": "Azul",
			"blue-green": "Azul e Verde",
			"green": "Verde",
			"brown-jr": "Castanho Junior",
			"brown": "Castanho",
			"black-jr": "Preto Junior",
			"black": "Preto",
			"duan-1": "Duan 1",
			"duan-2": "Duan 2",
			"duan-3": "Duan 3+",
		},
	}
}
</i18n>
