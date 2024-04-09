<template>
	<Loading v-if="loading" />
	<div v-else class="w-full max-w-xl mx-auto">
		<RadioGroupInput
			name="competition-select"
			:label="t('selectCompetition')"
			:radio-options="competitions"
			:option-selected="competition"
			:error="''"
			:columns="1"
			@selected="(option) => (competition = option)" />
		<router-link
			v-if="competition != null"
			:to="
				store.getters.getUserRole == 'MICRO'
					? { name: 'Microphone', params: { competitionId: competition } }
					: store.getters.getUserRole == 'PODIUM'
					? { name: 'Podium', params: { competitionId: competition } }
					: { name: 'Combat Manager', params: { competitionId: competition } }
			">
			<Button class="mt-8" :message="t('continue')" type="primary" @button-click="null" />
		</router-link>
		<Tooltip v-else :text="t('tooltips.competitionSelect')" class="mt-8">
			<Button
				class="opacity-50 pointer-events-none"
				:message="t('continue')"
				type="primary"
				@button-click="null" />
		</Tooltip>
	</div>
</template>
<script setup>
import Tooltip from "@/components/partials/templates/tooltip.vue";
import Loading from "@/components/partials/loading.vue";
import RadioGroupInput from "@/components/partials/inputs/radioGroup.vue";
import Button from "@/components/partials/button.vue";
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { authApi } from "@/services/api";
import toast from "@/toast.js";
import store from "@/store";

let { t } = useI18n({ useScope: "global" });
let competitions = ref([]);
let competition = ref(null);
let loading = ref(true);

authApi
	.get("competitions/all")
	.then((response) => {
		const today = new Date();
		for (let competition of response.data) {
			let endDate = new Date(competition.competition_end);
			endDate.setDate(endDate.getDate() + 1);
			if (new Date(competition.competition_start) <= today && endDate >= today) {
				competitions.value = [{ value: competition.id, name: competition.name }];
				break;
			}
			if (competition.name == "DEFAULTS") continue;
			competitions.value.push({ value: competition.id, name: competition.name });
		}
		loading.value = false;
	})
	.catch((error) => {
		console.error("Error Getting Competitions", error);
		toast.error("notFound.competition", 2);
		loading.value = false;
	});
</script>
