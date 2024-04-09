<template>
	<div class="p-2 z-10 relative bg-gray-200">
		<div class="inline-flex gap-x-10">
			<div class="grid">
				<label for="number" class="text-sm max-w-max">{{ t("match") }}</label>
				<input
					v-model="state.number"
					name="number"
					type="number"
					class="text-center w-20"
					@input="emit('number', state.number)" />
			</div>
			<div class="grid">
				<label for="number" class="text-sm max-w-max">{{ t("area") }}</label>
				<input
					v-model="state.areaNumber"
					type="number"
					class="text-center w-20"
					@input="emit('area', state.areaNumber)" />
			</div>
			<div class="grid">
				<label for="number" class="text-sm max-w-max">{{ t("points") }}</label>
				<input
					v-model="state.areaNumber"
					type="number"
					class="text-center w-20"
					@input="emit('area', state.points)" />
			</div>
		</div>
		<div class="tournament-athlete rounded-t-md before:bg-red-500">
			<input
				v-model="state.red_name"
				type="text"
				class="text-center"
				@input="emit('red', state.red_name)" />
		</div>
	</div>
</template>

<script setup>
import { ref, watch } from "vue";
import { getAthleteNameTeam } from "@/services/athlete.service.js";
import { useI18n } from "vue-i18n";

let { t } = useI18n();
let state = ref({
	areaNumber: props.match.number_by_area,
	number: props.match.number,
	red_name: getAthleteNameTeam(props.match.athlete_red),
	points: props.match.points_red_total,
});

const props = defineProps({
	match: {
		type: Object,
		required: true,
	},
	update: {
		type: Boolean,
		required: true,
	},
});

watch(
	() => props.update,
	() => {
		if (props.update) {
			state.value = {
				areaNumber: props.match.number_by_area,
				number: props.match.number,
				red_name: getAthleteNameTeam(props.match.athlete_red),
				blue_name: getAthleteNameTeam(props.match.athlete_blue),
				winner: props.match.winner_id == null ? "" : getAthleteNameTeam(props.match.winner),
			};
		}
		emit("updated");
	}
);

const emit = defineEmits(["number", "area", "red", "blue", "winner", "updated"]);
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
