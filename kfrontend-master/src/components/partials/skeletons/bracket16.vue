<template>
	<div class="relative min-w-[100vw] print:w-[1920px] min-h-[100vh] print:h-[1080px]">
		<div class="inline-flex w-[80vw] print:w-[1536px] justify-between">
			<div class="ml-4 font-bold text-3xl mt-2">
				{{ getTournamentName(tournament, t) }}
			</div>
			<div class="ml-auto font-medium text-xl mt-4">
				{{
					"D" +
					(tournament.day == null ? "" : tournament.day) +
					" - A" +
					(tournament.area == null ? "" : tournament.area) +
					" - " +
					(tournament.morning ? t("morning") : t("afternoon"))
				}}
			</div>
		</div>
		<div class="bg-white p-2">
			<div class="flex flex-row mt-4 space-x-10">
				<p class="w-[25rem] tournament-stage">{{ t("octo") }}</p>
				<p class="w-[25rem] tournament-stage relative top-14">{{ t("quarter") }}</p>
				<p class="w-[25rem] tournament-stage relative top-40">{{ t("semi") }}</p>
				<p class="w-[25rem] tournament-stage relative top-96">{{ t("final") }}</p>
			</div>
			<div class="flex flex-row bg-white space-x-10">
				<div class="flex flex-col space-y-6">
					<SingleMatch
						:tournament="props.tournament"
						:after-bracket-type="'small|top'"
						:number="1"
						:width="width" />
					<SingleMatch
						:tournament="props.tournament"
						:after-bracket-type="'small|bot'"
						:number="2"
						:width="width" />
					<SingleMatch
						:tournament="props.tournament"
						:after-bracket-type="'small|top'"
						:number="3"
						:width="width" />
					<SingleMatch
						:tournament="props.tournament"
						:after-bracket-type="'small|bot'"
						:number="4"
						:width="width" />
					<SingleMatch
						:tournament="props.tournament"
						:after-bracket-type="'small|top'"
						:number="5"
						:width="width" />
					<SingleMatch
						:tournament="props.tournament"
						:after-bracket-type="'small|bot'"
						:number="6"
						:width="width" />
					<SingleMatch
						:tournament="props.tournament"
						:after-bracket-type="'small|top'"
						:number="7"
						:width="width" />
					<SingleMatch
						:tournament="props.tournament"
						:after-bracket-type="'small|bot'"
						:number="8"
						:width="width" />
				</div>

				<div class="flex flex-col">
					<div class="h-[55px]" />
					<SingleMatch
						:tournament="props.tournament"
						:before-bracket-type="'small0-5'"
						:after-bracket-type="'medium|top'"
						:number="9"
						:width="width" />
					<div class="h-[130px]" />
					<SingleMatch
						:tournament="props.tournament"
						:before-bracket-type="'small0-5'"
						:after-bracket-type="'medium|bot'"
						:number="10"
						:width="width" />
					<div class="h-[130px]" />
					<SingleMatch
						:tournament="props.tournament"
						:before-bracket-type="'small0-5'"
						:after-bracket-type="'medium|top'"
						:number="11"
						:width="width" />
					<div class="h-[130px]" />
					<SingleMatch
						:tournament="props.tournament"
						:before-bracket-type="'small0-5'"
						:after-bracket-type="'medium|bot'"
						:number="12"
						:width="width" />
				</div>

				<div class="flex flex-col">
					<div class="h-[165px]" />
					<SingleMatch
						:tournament="props.tournament"
						:before-bracket-type="'small0-5'"
						:after-bracket-type="'big|top'"
						:number="13"
						:width="width" />
					<div class="h-[350px]" />
					<SingleMatch
						:tournament="props.tournament"
						:before-bracket-type="'small0-5'"
						:after-bracket-type="'big|bot'"
						:number="14"
						:width="width" />
				</div>

				<div class="flex flex-col">
					<div class="h-[388px]" />
					<SingleMatch
						:tournament="props.tournament"
						:before-bracket-type="'small'"
						:number="15"
						:width="width" />
					<div class="h-[5rem]" />
					<SingleMatch
						:tournament="props.tournament"
						:before-bracket-type="'third'"
						:number="16"
						:width="width" />
				</div>
			</div>
		</div>
		<div class="absolute top-10 right-20">
			<Podium :tournament="props.tournament" />
		</div>
		<div class="absolute bottom-10 right-20 w-1/2">
			<Judges
				:judge1="props.tournament.judge1"
				:judge2="props.tournament.judge2"
				:central="props.tournament.central_referee" />
		</div>
	</div>
</template>

<script setup>
import Judges from "@/components/partials/skeletons/judges.vue";
import Podium from "@/components/partials/skeletons/podium.vue";
import SingleMatch from "@/components/partials/skeletons/singleMatch.vue";
import { getTournamentName } from "@/services/competition.service.js";
import { useI18n } from "vue-i18n";

let { t } = useI18n();

const width = 25;

const props = defineProps({
	tournament: {
		type: Object,
		required: true,
	},
});
</script>

<i18n>
{
	"en_GB": {
		"open": "Open",
		"masc": "Masculine",
		"fem": "Feminine",
		"year": "{count} Year | {count} Years",
		"octo": "Round of 16",
		"quarter": "Quarter-finals",
		"semi": "Semi-finals",
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
		"octo": "Oitavos de final",
		"quarter": "Quartos de final",
		"semi": "Semi-finais",
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
