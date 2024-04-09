<template>
	<div class="w-full">
		<h3 class="text-xl font-semibold text-center">{{ t(`placeNumber.${props.place}`) }}</h3>
		<div class="flex flex-col gap-y-2">
			<router-link
				:to="{ name: 'Show Tournament', params: { tournament: tournament.id } }"
				v-for="tournament in props.tournaments"
				:key="tournament.id"
				:class="[
					'rounded-xl w-full py-1 px-4 hover:brightness-[.85] text-center whitespace-pre-line',
					props.place == 1
						? 'bg-[#FFD700]'
						: props.place == 2
						? 'bg-[#BFBFBF]'
						: props.place == 3
						? 'bg-[#CD7F32]'
						: 'bg-blue-500',
				]">
				{{ `${tournament.competition_name}\n${getTournamentName(tournament, t)}` }}
			</router-link>
		</div>
	</div>
</template>
<script setup>
import { getTournamentName } from "@/services/competition.service.js";
import { useI18n } from "vue-i18n";

let { t } = useI18n({ useScope: "global" });
const props = defineProps({
	tournaments: {
		type: Array,
		required: true,
	},
	place: {
		type: Number,
		required: true,
	},
});
</script>
