<template>
	<Modal :open="open" :outsideClick="false" @close="emit('close')">
		<p class="text-3xl text-center font-semibold">
			{{ t("numberMatchesForCompetition", { name: props.competitionName }) }}
		</p>
		<div v-if="beingProcessed || finishProcessing" class="mt-4">
			<p v-if="!finishProcessing" class="text-2xl text-center font-medium">
				{{ t("processingTournaments") }}
			</p>
			<div class="text-center">
				<div v-if="finishProcessing">
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
							t("renumeringMatchesCompetition", {
								day: current.day,
								time: t(current.time),
								area: current.area,
							})
						}}
					</p>
				</div>
				<div v-if="failed.length" class="flex flex-col">
					<p v-for="fail of failed" class="text-lg font-medium">
						{{
							t("failedRenumeringMatches", {
								day: fail.day,
								time: t(fail.time),
								area: fail.area,
							})
						}}
					</p>
				</div>
			</div>
		</div>
		<div v-else class="mt-10">
			<div class="mt-10 mx-auto max-w-max">
				<Button
					:message="t('numberMatches')"
					type="primary"
					@button-click="startNumberingMatches" />
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
import { authApi } from "@/services/api";

const { t } = useI18n({ useScope: "global" });

const days = ref(3);
const times = ref(["morning", "afternoon"]);
const areas = ref(12);
const current = ref({ day: 1, time: "", area: 1 });

const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	competitionId: {
		type: String,
		required: true,
	},
	competitionName: {
		type: String,
		required: true,
	},
});
const emit = defineEmits(["close"]);
const failed = ref([]);
const beingProcessed = ref(false);
const finishProcessing = ref(false);

watch(
	() => props.open,
	() => {
		if (finishProcessing.value && props.open) {
			finishProcessing.value = false;
		}
	}
);

const startNumberingMatches = async () => {
	beingProcessed.value = true;
	for (let day = 1; day <= days.value; day++) {
		for (const time of times.value) {
			for (let area = 1; area <= areas.value; area++) {
				try {
					current.value = { day: day, time: time, area: area };
					const response = await authApi.post(
						`competitions/${
							props.competitionId
						}/tournaments/renumber?day=${day}&morning=${
							time === "morning" ? "true" : "false"
						}&area=${area}`
					);
				} catch {
					failed.value.push({ day: day, time: time, area: area });
				}
			}
		}
	}
	beingProcessed.value = false;
	finishProcessing.value = true;
};
</script>
