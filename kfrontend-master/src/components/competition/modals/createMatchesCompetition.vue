<template>
	<Modal :open="open" :outsideClick="false" @close="emit('close')">
		<p class="text-3xl text-center font-semibold">
			{{ t("createMatchesForCompetition", { name: competitionName }) }}
		</p>
		<div v-if="beingProcessed || finishedProcessing" class="mt-4">
			<div v-if="settingUpTournaments">
				<p class="text-2xl text-center font-medium">
					{{ t("preparingTournamentsToCreateMatches") }}
				</p>
				<Loading :size="5" class="mx-auto" />
			</div>
			<div v-else>
				<p v-if="!finishedProcessing" class="text-2xl text-center font-medium">
					{{ t("processingTournaments") }}
				</p>
				<div class="text-center">
					<div v-if="finishedProcessing">
						<CheckCircleIcon class="w-10 h-10 mx-auto" />
						<p class="text-xl font-medium">
							{{ t("finished") }}
						</p>
					</div>
					<div v-else>
						<p class="text-xl text-center font-medium text-red-500">
							{{ t("doNotCloseModal") }}
						</p>
						<Loading :size="5" class="mx-auto" />
						<p class="text-lg">
							{{
								t("recreatingTournamentCompetition", {
									atual: numberProcessed,
									total: tournamentIDs.length,
								})
							}}
						</p>
					</div>
					<div v-if="failed.length" class="flex flex-col">
						<p class="text-lg font-medium">{{ t("failedCreatingMatches") }}</p>
						<router-link
							v-for="id of failed"
							:key="id"
							:to="{ name: 'Show Tournament', params: { tournament: id } }"
							target="_blank"
							class="text-lg link">
							{{ t("tournamentId", { id: id }) }}
						</router-link>
					</div>
				</div>
			</div>
		</div>
		<div v-else class="mt-10">
			<p class="text-3xl text-center font-bold mb-4 text-red-500">
				{{ t("thisActionWillDeleteAllMatchesAndPreviousResults") }}
			</p>
			<div class="mt-10 mx-auto max-w-max">
				<Button
					:message="t('createMatches')"
					type="primary"
					@button-click="startCreatingMatches" />
			</div>
		</div>
	</Modal>
</template>

<script setup>
import Button from "@/components/partials/button.vue";
import Modal from "@/components/partials/modal.vue";
import Loading from "@/components/partials/loading.vue";
import { CheckCircleIcon } from "@heroicons/vue/24/outline";
import { useI18n } from "vue-i18n";
import { ref, watch } from "vue";
import { authApi, errorHandling } from "@/services/api";

const { t } = useI18n({ useScope: "global" });

const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	competitionId: {
		type: String,
		required: true,
	},
});
const emit = defineEmits(["close"]);
const numberProcessed = ref(0);
const failed = ref([]);
const beingProcessed = ref(false);
const finishedProcessing = ref(false);
const settingUpTournaments = ref(false);
const tournamentIDs = ref([]);
const competitionName = ref("");

watch(
	() => props.open,
	() => {
		if (finishProcessing.value && props.open) {
			finishProcessing.value = false;
		}
	}
);

const startCreatingMatches = async () => {
	beingProcessed.value = true;
	settingUpTournaments.value = true;
	try {
		const { data } = await authApi.get(`competitions/${props.competitionId}`);
		tournamentIDs.value = data.tournaments.map((tournament) => tournament.id);
		competitionName.value = data.name;
	} catch (e) {
		errorHandling(e);
		beingProcessed.value = false;
		settingUpTournaments.value = false;
		return;
	}
	settingUpTournaments.value = false;

	numberProcessed.value = 0;
	beingProcessed.value = true;
	for (const id of tournamentIDs.value) {
		try {
			const response = await authApi.post(`tournaments/${id}/recreate`);
		} catch {
			failed.value.push(id);
		} finally {
			numberProcessed.value += 1;
		}
	}
	beingProcessed.value = false;
	finishedProcessing.value = true;
};
</script>
