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
							<p
								v-if="props.match != null"
								class="text-xl font-semibold text-center mb-4">
								{{ t("callAthlete", numberAthletes) }}
							</p>
							<div v-if="props.match != null" class="relative">
								<p class="text-lg font-medium">
									{{
										`${t("areaNumber", {
											number: props.match.area_to_call,
										})} ${t("matchNum", {
											number: props.match.number_by_area,
										})}`
									}}
								</p>
								<p>{{ t("athlete.self", numberAthletes) }}</p>
								<div class="inline-flex w-full space-x-4">
									<div
										v-if="props.match.athlete_red_id"
										class="rounded bg-red-400 px-2 py-0.5 w-full text-center capitalize">
										<p v-if="props.match?.athlete_blue_id">
											{{ t("redCorner") }}
										</p>
										<p>
											{{ getAthleteNameTeam(props.match.athlete_red) }}
										</p>
									</div>
									<div
										v-if="props.match.athlete_blue_id"
										class="rounded bg-blue-400 px-2 py-0.5 w-full text-center capitalize">
										<p>{{ t("blueCorner") }}</p>
										<p>
											{{ getAthleteNameTeam(props.match.athlete_blue) }}
										</p>
									</div>
								</div>
								<p>
									{{
										t("requests", {
											count: props.match.number_call_request,
										})
									}}
								</p>
								<p>{{ t("callsMade", { count: props.match.calls_made }) }}</p>
								<div class="inline-flex mt-4">
									<p>{{ t("callType") }}</p>
									<p class="ml-1 font-medium">
										{{
											["c", "p", "s", "l"].findIndex(
												(a) => a == match.call_type
											) === -1
												? t("microphone.callType.otherCall", {
														call: match.call_type,
												  })
												: t(`microphone.callType.${match.call_type}`)
										}}
									</p>
								</div>
								<div class="space-y-4 mt-4">
									<div>
										<p class="font-medium">{{ t("notes.previous") }}</p>
										<p
											class="px-2 ml-2 mr-2 py-1 bg-blue-50 rounded whitespace-pre-line">
											{{ props.match.description_to_micro || t("notes.no") }}
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
										:message="t('callAthlete', numberAthletes)"
										@button-click="callMade()" />
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
import TextAreaInput from "@/components/partials/inputs/textAreaInput.vue";
import Button from "@/components/partials/button.vue";
import { useI18n } from "vue-i18n";
import { ref, watch, computed } from "vue";
import { authApi } from "@/services/api";
import toast from "@/toast.js";
import { getAthleteNameTeam } from "@/services/athlete.service";

let { t } = useI18n({ useScope: "global" });
const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	match: {
		type: Object,
		required: false,
		default: null,
	},
});
const emit = defineEmits(["close", "sent"]);
let open = ref(props.open);
let showLoading = ref(false);
let showX = ref(false);
let notes = ref("");
let numberAthletes = computed(
	() =>
		Number(props.match?.athlete_red_id !== null) + Number(props.match?.athlete_blue_id !== null)
);

watch(
	() => props.open,
	(after) => {
		if (after && props.match == null) {
			toast.error(t("m.noMatch"));
			return;
		}
		if (after) {
			notes.value = "";
		}
		open.value = after;
	}
);

function callMade() {
	showLoading.value = true;
	showX.value = false;
	authApi
		.put(`matches/call-made/${props.match.id}`, {
			description_to_micro: notes.value,
		})
		.then(() => {
			showLoading.value = false;
			emit("sent");
			emit("close");
		})
		.catch((error) => {
			showLoading.value = false;
			showX.value = true;
			toast.error(t("notFound.match"));
			console.error(error);
		});
}
</script>
