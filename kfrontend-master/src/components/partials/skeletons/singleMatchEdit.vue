<template>
	<div class="p-2 relative bg-gray-200">
		<div class="inline-flex gap-x-10">
			<div class="flex flex-col">
				<label for="number" class="text-sm max-w-max">{{ t("match") }}</label>
				<div class="w-20 border border-black bg-white text-center h-full">
					<p class="relative top-1/2 -translate-y-1/2">
						{{ match.number }}
					</p>
				</div>
			</div>
			<div class="grid">
				<label for="number" class="text-sm max-w-max">{{ t("area") }}</label>
				<input
					v-model="state.areaNumber"
					type="number"
					class="text-center w-20"
					@input="emit('area', state.areaNumber)" />
			</div>
		</div>
		<div class="tournament-athlete rounded-t-md before:bg-red-500">
			<input
				v-model="state.red_name"
				type="text"
				class="text-center"
				@input="emit('red', state.red_name)" />
		</div>
		<div class="tournament-athlete before:bg-blue-500">
			<input
				v-model="state.blue_name"
				type="text"
				class="text-center"
				@input="emit('blue', state.blue_name)" />
		</div>
		<div class="tournament-athlete rounded-b-md before:bg-yellow-500 grid">
			<label for="winner" class="text-sm ml-5 max-w-max">{{ t("winner") }}</label>
			<input
				v-model="state.winner"
				name="winner"
				type="text"
				class="text-center"
				@input="emit('winner', state.winner)" />
		</div>
	</div>
</template>

<script setup>
import { ref } from "vue";
import { getAthleteNameTeam } from "@/services/athlete.service.js";
import { useI18n } from "vue-i18n";

let { t } = useI18n();
const props = defineProps({
	match: {
		type: Object,
		required: true,
	},
});
let state = ref({
	areaNumber: props.match.number_by_area,
	number: props.match.number,
	red_name: getAthleteNameTeam(props.match.athlete_red),
	blue_name: getAthleteNameTeam(props.match.athlete_blue),
	winner: getAthleteNameTeam(props.match.winner) || "",
});

const emit = defineEmits(["number", "area", "red", "blue", "winner"]);
</script>

<i18n>
{
	"en_GB": {
		"match": "Match Number",
		"area": "Area Number",
		"winner": "Winner",
	},
	"pt_PT": {
		"match": "Número do combate",
		"area": "Número da área",
		"winner": "Vencedor",
	},
}
</i18n>
