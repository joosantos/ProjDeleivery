<template>
	<div>
		<TransitionRoot as="template" :show="open">
			<Dialog as="div" class="fixed z-20 inset-0 overflow-y-auto" @close="emit('close')">
				<div
					class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
					<TransitionChild
						as="template"
						enter="ease-out duration-300"
						enter-from="opacity-0"
						enter-to="opacity-100"
						leave="ease-in duration-200"
						leave-from="opacity-100"
						leave-to="opacity-0">
						<DialogOverlay
							class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
					</TransitionChild>

					<!-- This element is to trick the browser into centering the modal contents. -->
					<span
						class="hidden sm:inline-block sm:align-middle sm:h-screen"
						aria-hidden="true"
						>&#8203;</span
					>
					<TransitionChild
						as="template"
						enter="ease-out duration-300"
						enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
						enter-to="opacity-100 translate-y-0 sm:scale-100"
						leave="ease-in duration-200"
						leave-from="opacity-100 translate-y-0 sm:scale-100"
						leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
						<div
							class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
							<Loading v-if="loading" :size="10" />
							<div v-else>
								<p class="text-xl font-semibold text-center mb-4">
									{{ t("tournamentPrinted") }}
								</p>
								<div v-if="tournament != null" class="relative space-y-2">
									<p class="text-lg font-medium text-center">
										{{ props.tournamentName }}
									</p>
									<p
										v-if="tournament.first_place_id"
										class="px-2 py-1 bg-[#FFD700] rounded">
										{{ `1º- ${getAthleteNameTeam(tournament.first_place)}` }}
									</p>
									<p
										v-if="tournament.second_place_id"
										class="px-2 py-1 bg-[#BFBFBF] rounded">
										{{ `2º- ${getAthleteNameTeam(tournament.second_place)}` }}
									</p>
									<p
										v-if="tournament.third_place_id"
										class="px-2 py-1 bg-[#CD7F32] rounded">
										{{ `3º- ${getAthleteNameTeam(tournament.third_place)}` }}
									</p>
									<div>
										<p class="font-medium">{{ t("notes.previous") }}</p>
										<p
											class="px-2 ml-2 mt-2 mr-2 py-1 bg-blue-50 rounded whitespace-pre-line">
											{{ tournament.podium_notes || t("notes.no") }}
										</p>
									</div>
									<TextAreaInput
										:label="t('notes.additional')"
										type="text"
										:name="'notes'"
										:option-selected="notes"
										:error="''"
										@value-changed="(option) => (notes = option)" />
									<Button
										:type="'primary'"
										:loading="showLoading"
										:show-x="showX"
										:message="t('markTournamentPrinted')"
										@button-click="printed()" />
								</div>
							</div>
						</div>
					</TransitionChild>
				</div>
			</Dialog>
		</TransitionRoot>
	</div>
</template>

<script setup>
import { Dialog, DialogOverlay, TransitionChild, TransitionRoot } from "@headlessui/vue";
import Loading from "@/components/partials/loading.vue";
import Button from "@/components/partials/button.vue";
import TextAreaInput from "@/components/partials/inputs/textAreaInput.vue";
import { useI18n } from "vue-i18n";
import { ref, watch } from "vue";
import { authApi } from "@/services/api";
import toast from "@/toast.js";
import { getAthleteNameTeam } from "@/services/athlete.service";

const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	tournamentId: {
		type: String,
		required: false,
		default: "",
	},
	tournamentName: {
		type: String,
		required: false,
		default: "",
	},
});

let { t } = useI18n({ useScope: "global" });
let open = ref(props.open);
let showLoading = ref(false);
let showX = ref(false);
let loading = ref(false);
let tournament = ref(null);
let notes = ref("");
const emit = defineEmits(["close", "sent"]);

watch(
	() => props.open,
	(after) => {
		if (after && props.tournamentId === "") {
			toast.error(t("notFound.tournament", 1));
			emit("close");
			return;
		}
		if (after) {
			loading.value = true;
			authApi
				.get(`tournaments/${props.tournamentId}/print-podium`)
				.then((response) => {
					tournament.value = response.data;
					loading.value = false;
				})
				.catch((error) => {
					console.error("Error Getting Tournaments", error);
					toast.error(t("notFound.tournament", 1));
					loading.value = false;
					showLoading.value = false;
				});
		}
		notes.value = "";
		open.value = after;
	}
);

function printed() {
	showLoading.value = true;
	showX.value = false;
	authApi
		.put(`tournaments/${tournament.value.id}/printed`, {
			podium_notes: notes.value,
		})
		.then(() => {
			showLoading.value = false;
			emit("sent");
			emit("close");
		})
		.catch((error) => {
			showLoading.value = false;
			showX.value = true;
			toast.error(t("m.noTournament"));
			console.error(error);
		});
}
</script>
