<template>
	<div
		class="p-4 bg-gray-50 border border-gray-300 rounded-xl"
		v-if="Object.keys(inscriptionsStore.getters.getUpdates).length">
		<Confirmation
			:title="t('clearChangesHistory')"
			:message="t('clearChangesHistory')"
			:buttonText="t('clear')"
			:open="showClearConfirmation"
			@close="closeConfirmation"
			@deleted="deleteUpdates" />
		<Button
			class="max-w-max mb-4 mt-2"
			:message="t('clearChangesHistory')"
			type="primary"
			size="small"
			@button-click="openConfirmation" />

		<div v-for="{ team, updates } of inscriptionsStore.getters.getUpdates">
			<h2 class="text-xl font-semibold">
				<b>{{ team.name }} ({{ team.abbreviation }})</b>
			</h2>
			<ul>
				<li
					v-for="{ athletes, newTournament, oldTournament } of updates"
					class="list-disc ml-8">
					<p>
						{{ t("inscriptionsUpdates.athlete") }}
						{{ getAthletesNameFromArray(athletes) }}
						{{ t("inscriptionsUpdates.movedFrom") }}
						<router-link
							:to="{
								name: 'Show Tournament',
								params: { tournament: oldTournament.id },
							}"
							class="link">
							{{ getTournamentNameChange(oldTournament) }}
						</router-link>
						{{ t("inscriptionsUpdates.to") }}
						<router-link
							:to="{
								name: 'Show Tournament',
								params: { tournament: newTournament.id },
							}"
							class="link">
							{{ getTournamentNameChange(newTournament) }}
						</router-link>
					</p>
				</li>
			</ul>
		</div>
	</div>
</template>

<script setup>
import { ref } from "vue";
import Button from "@/components/partials/button.vue";
import Confirmation from "@/components/partials/messages/confirmation.vue";
import inscriptionsStore from "@/stores/inscriptions.js";
import { getTournamentName } from "@/services/competition.service.js";
import { getAthletesNameFromArray } from "@/services/athlete.service.js";
import { useI18n } from "vue-i18n";

const { t } = useI18n({ useScope: "global" });

const showClearConfirmation = ref(false);

const getTournamentNameChange = (tournament) => {
	return getTournamentName(tournament, t);
};

const openConfirmation = () => {
	showClearConfirmation.value = true;
};
const closeConfirmation = () => {
	showClearConfirmation.value = false;
};
const deleteUpdates = () => {
	showClearConfirmation.value = false;
	inscriptionsStore.commit("clearUpdates");
};
</script>
