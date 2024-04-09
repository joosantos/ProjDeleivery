<template>
	<div
		v-for="match of props.matches"
		:key="`${match.id}${match.updated_at}`"
		class="px-4 py-2 pb-4 bg-blue-100 hover:bg-blue-200 cursor-pointer rounded-xl w-full space-y-2 group"
		@click="emit('openModal', match)">
		<div class="inline-flex justify-between w-full">
			<p>
				{{
					`${t("areaNumber", {
						number: match.area_to_call,
					})} ${t("matchNum", {
						number: match.number_by_area,
					})}`
				}}
			</p>
			<p>
				{{
					["c", "p", "s", "l"].findIndex((a) => a == match.call_type) === -1
						? t("microphone.callType.otherCall", {
								call: match.call_type,
						  })
						: t(`microphone.callType.${match.call_type}`)
				}}
			</p>
		</div>
		<div v-if="match.description_to_micro">
			<p>{{ t("notes.self", 2) }}</p>
			<p
				class="bg-yellow-500 group-hover:bg-blue-100 rounded ml-4 px-2 py-0.5 whitespace-pre-line">
				{{ match.description_to_micro || t("notes.no") }}
			</p>
		</div>
		<p class="bg-red-400 px-2 py-0.5 rounded text-center">
			{{
				match?.athlete_blue_id
					? `${t("redCorner")} ${getAthleteNameTeam(match.athlete_red)}`
					: getAthleteNameTeam(match.athlete_red)
			}}
		</p>
		<p v-if="match?.athlete_blue_id" class="bg-blue-400 px-2 py-0.5 rounded text-center">
			{{ `${t("blueCorner")} ${getAthleteNameTeam(match.athlete_blue)}` }}
		</p>
	</div>
</template>

<script setup>
import { useI18n } from "vue-i18n";
import { getAthleteNameTeam } from "@/services/athlete.service";
let { t } = useI18n({ useScope: "global" });
const emit = defineEmits(["openModal"]);
const props = defineProps({
	matches: {
		type: Array,
		required: true,
	},
});
</script>
