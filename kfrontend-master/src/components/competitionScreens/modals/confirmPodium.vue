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
							<div>
								<p class="text-xl font-semibold text-center mb-4">
									{{ t("confirmPodium") }}
								</p>
								<div class="space-y-4">
									<div class="bg-[#FFD700] p-2 rounded-xl border border-black">
										<SearchSelect
											:title="t('podium.first')"
											:options="athletes"
											:option-selected="first"
											:error="''"
											:readonly="false"
											@selected="(option) => (first = option)" />
									</div>
									<div class="bg-[#BFBFBF] p-2 rounded-xl border border-black">
										<SearchSelect
											:title="t('podium.second')"
											:options="athletes"
											:option-selected="second"
											:error="''"
											:readonly="false"
											@selected="(option) => (second = option)" />
									</div>
									<div class="bg-[#CD7F32] p-2 rounded-xl border border-black">
										<SearchSelect
											:title="t('podium.third')"
											:options="athletes"
											:option-selected="third"
											:error="''"
											:readonly="false"
											@selected="(option) => (third = option)" />
									</div>
									<div v-if="tournament?.podium_notes != null">
										<p class="font-medium">{{ t("notes.previous") }}</p>
										<p
											class="px-2 ml-2 mr-2 py-1 bg-blue-50 rounded whitespace-pre-line">
											{{ tournament.podium_notes || t("notes.no") }}
										</p>
									</div>
									<div>
										<TextAreaInput
											:label="t('notes.additional')"
											type="text"
											:name="'notes'"
											:option-selected="notes"
											:error="''"
											@value-changed="(option) => (notes = option)" />
									</div>
									<CustomInput
										:label="t('nextMatchNumber')"
										type="text"
										:name="'nextMatchNumber'"
										:option-selected="number"
										:error="''"
										@value-changed="(option) => (number = option)" />
									<div
										v-if="
											tournament?.category?.category_type?.name !=
											'Tournament'
										"
										class="relative max-w-max left-1/2 -translate-x-1/2 mt-10">
										<Button
											:type="'primary'"
											:message="t('showPodium')"
											:submit="true"
											@button-click="updateTournament(true)" />
									</div>
									<div class="relative max-w-max left-1/2 -translate-x-1/2 mt-10">
										<Button
											:type="'primary'"
											:message="
												tournament?.category?.category_type?.name !=
												'Tournament'
													? t('onlyLoadNextMatch')
													: t('loadNextMatch')
											"
											:submit="true"
											@button-click="updateTournament(false)" />
									</div>
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
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import TextAreaInput from "@/components/partials/inputs/textAreaInput.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import Button from "@/components/partials/button.vue";
import { useI18n } from "vue-i18n";
import { ref, watch } from "vue";
import { authApi } from "@/services/api";
import toast from "@/toast.js";
import { getAthleteNameTeam } from "@/services/athlete.service";

let { t } = useI18n({ useScope: "global" });
let open = ref(false);
let loading = ref(true);
let tournament = ref(null);
let athletes = ref([]);
let first = ref("");
let second = ref("");
let third = ref("");
let number = ref("");
let notes = ref("");
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
	number: {
		type: String,
		required: true,
	},
});
const emit = defineEmits(["close", "next", "showPodium"]);

watch(
	() => props.open,
	(after) => {
		open.value = after;
		if (!after || props.tournamentId === "") {
			return;
		}
		loading.value = true;
		tournament.value = null;
		number.value = props.number;
		athletes.value = [{ id: "", name: t("none") }];
		authApi
			.get(`tournaments/table/${props.tournamentId}`)
			.then((response) => {
				tournament.value = response.data;
				for (let match of tournament.value.matches) {
					let index =
						match.athlete_red_id == null
							? 0
							: athletes.value.findIndex((a) => a.id == match.athlete_red_id);
					if (index == -1) {
						athletes.value.push({
							id: match.athlete_red_id,
							name: getAthleteNameTeam(match.athlete_red),
						});
					}
					index =
						match.athlete_blue_id == null
							? 0
							: athletes.value.findIndex((a) => a.id == match.athlete_blue_id);
					if (index == -1) {
						athletes.value.push({
							id: match.athlete_blue_id,
							name: getAthleteNameTeam(match.athlete_blue),
						});
					}
				}
				first.value = tournament.value.first_place_id || "";
				second.value = tournament.value.second_place_id || "";
				third.value = tournament.value.third_place_id || "";
				notes.value = "";
				loading.value = false;
			})
			.catch((error) => {
				console.log(error);
				toast.error(t("error.podiumUpdate"));
				loading.value = false;
			});
	}
);

function updateTournament(emitShow) {
	authApi
		.put(`tournaments/podium/${props.tournamentId}`, {
			first: first.value || null,
			second: second.value || null,
			third: third.value || null,
			podium_notes: notes.value || null,
		})
		.then(() => {
			let firstName = athletes.value.find((a) => a.id == first.value)?.name || null;
			if (firstName == t("none")) firstName = null;
			let secondName = athletes.value.find((a) => a.id == second.value)?.name || null;
			if (secondName == t("none")) secondName = null;
			let thirdName = athletes.value.find((a) => a.id == third.value)?.name || null;
			if (thirdName == t("none")) thirdName = null;
			if (emitShow) emit("showPodium", firstName, secondName, thirdName);
			else emit("next", number.value);
			emit("close");
		})
		.catch((error) => {
			toast.error(t("error.podiumUpdate"));
			console.error("Error Updating Podium", error);
		});
}
</script>
