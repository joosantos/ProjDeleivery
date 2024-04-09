<template>
	<div class="w-[30rem]">
		<div class="p-2 z-10 relative">
			<div
				class="tournament-athlete rounded-md before:hidden inline-flex justify-center w-full bg-[#FFD700]">
				<p class="mr-auto ml-2 text-lg font-medium">1º</p>
				<p class="mr-auto">
					{{
						props.tournament.first_place_id == null
							? "____________________________________________"
							: getAthleteNameTeam(props.tournament.first_place)
					}}
				</p>
			</div>
		</div>
		<div
			v-if="
				props.tournament.matches.length > 1 ||
				(props.tournament.matches[0].athlete_red_id != null &&
					props.tournament.matches[0].athlete_blue_id != null)
			"
			class="p-2 z-10 relative">
			<div
				class="tournament-athlete rounded-md before:hidden inline-flex justify-center w-full bg-[#BFBFBF]">
				<p class="mr-auto ml-2 text-lg font-medium">2º</p>
				<p class="mr-auto">
					{{
						props.tournament.second_place_id == null
							? "____________________________________________"
							: getAthleteNameTeam(props.tournament.second_place)
					}}
				</p>
			</div>
		</div>
		<div
			v-if="props.tournament.matches.length != 1 || props.tournament.third_place_id != null"
			class="p-2 z-10 relative">
			<div
				class="tournament-athlete rounded-md before:hidden inline-flex justify-center w-full bg-[#CD7F32]">
				<p class="mr-auto ml-2 text-lg font-medium">3º</p>
				<p class="mr-auto">
					{{
						props.tournament.third_place_id == null
							? "____________________________________________"
							: getAthleteNameTeam(props.tournament.third_place)
					}}
				</p>
			</div>
		</div>
		<div
			v-if="
				['ADMIN', 'AREA', 'PODIUM'].findIndex((a) => a == store.getters.getUserRole) !== -1
			"
			class="p-2 bg-blue-100 rounded z-10 relative whitespace-pre-line">
			<p>
				{{ t("notes") }}
			</p>
			<p>
				{{ props.tournament.podium_notes || t("noNotes") }}
			</p>
		</div>
	</div>
</template>

<script setup>
import { getAthleteNameTeam } from "@/services/athlete.service.js";
import store from "@/store";
import { useI18n } from "vue-i18n";
let { t } = useI18n();

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
        "notes": "Notes:",
        "noNotes": "No Notes",
	},
	"pt_PT": {
        "notes": "Notas:",
        "noNotes": "Sem Notas",
	}
}
</i18n>
