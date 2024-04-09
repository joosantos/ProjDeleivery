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
		<div class="bg-white px-2">
			<div class="flex flex-row space-x-10 mt-4 ml-2">
				<p class="w-[40rem] tournament-stage">{{ t("final") }}</p>
			</div>
			<div class="flex flex-row bg-white space-x-10">
				<SingleMatch :tournament="props.tournament" :number="1" :width="width" />
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

const width = 40;

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
