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
							<XCircleIcon
								v-if="match == null"
								class="w-10 h-10 text-gray-400 absolute top-4 right-6 hover:text-gray-600 cursor-pointer"
								@click="emit('close')" />
							<ArrowLeftCircleIcon
								v-else
								class="w-10 h-10 text-gray-400 absolute top-4 hover:text-gray-600 cursor-pointer"
								@click="match = null" />
							<p class="capitalize text-xl font-semibold text-center mb-4">
								{{ t("callAthlete", numberAthletes) }}
							</p>
							<div v-if="match == null">
								<div class="mb-4 w-1/2 space-y-2">
									<Button
										size="small"
										:type="'danger'"
										:capitalize="true"
										:message="t('callFireman')"
										@button-click="callSpecial('f')"
										@keypress.enter.prevent="null" />
									<Button
										size="small"
										:type="'success'"
										:capitalize="true"
										:message="t('callCleaning')"
										@button-click="callSpecial('c')"
										@keypress.enter.prevent="null" />
								</div>
								<CustomInput
									:label="t('area')"
									type="text"
									mask="##"
									:name="'area'"
									:option-selected="state.area.toString()"
									:error="''"
									@value-changed="(option) => (state.area = option)" />
								<CustomInput
									class="mt-4"
									:label="t('matchNumber')"
									type="text"
									:name="'matchNumber'"
									:option-selected="state.number.toString()"
									:error="''"
									@value-changed="(option) => (state.number = option)" />
								<Button
									class="mt-4"
									:type="'primary'"
									:loading="showLoading"
									:show-x="showX"
									:message="t('callThisMatch')"
									@button-click="callThis()" />
							</div>
							<div v-else class="relative">
								<p class="text-lg">{{ t("athlete.self", numberAthletes) }}</p>
								<div class="inline-flex w-full space-x-4">
									<div
										v-if="match.athlete_red_id"
										class="rounded bg-red-400 px-2 py-0.5 w-full text-center">
										<p v-if="numberAthletes === 2">{{ t("redCorner") }}</p>
										<p>
											{{ getAthleteNameTeam(match.athlete_red) }}
										</p>
									</div>
									<div
										v-if="match.athlete_blue_id"
										class="rounded bg-blue-400 px-2 py-0.5 w-full text-center">
										<p>{{ t("blueCorner") }}</p>
										<p>
											{{ getAthleteNameTeam(match.athlete_blue) }}
										</p>
									</div>
								</div>
								<div class="mt-2">
									<p>
										{{ t("requests", { count: match.number_call_request }) }}
									</p>
									<p>{{ t("callsMade", { count: match.calls_made }) }}</p>
								</div>
								<div class="space-y-4 mt-4">
									<RadioGroup
										:name="'callType'"
										:label="t('callType')"
										:capitalize-title="true"
										:radio-options="callTypes"
										:option-selected="state.callType"
										:error="''"
										:columns="2"
										@selected="(option) => (state.callType = option)" />
									<CustomInput
										v-if="state.callType === 'o'"
										:label="t('callTypes.otherType')"
										type="text"
										:name="'otherCallType'"
										:option-selected="state.callTypeOther"
										:error="''"
										@value-changed="
											(option) => (state.callTypeOther = option)
										" />
									<div v-if="match.number_call_request > 0">
										<p class="font-medium">{{ t("notes.previous") }}</p>
										<p
											class="px-2 ml-2 mr-2 py-1 bg-blue-50 rounded whitespace-pre-line">
											{{ match.description_to_micro || t("notes.no") }}
										</p>
									</div>
									<TextAreaInput
										:label="t('notes.additional')"
										type="text"
										:name="'notes'"
										:option-selected="state.notes"
										:error="''"
										@value-changed="(option) => (state.notes = option)" />
									<Tooltip
										v-if="match.number_call_request > match.calls_made"
										:text="t('callRequestTooltip')">
										<div class="pointer-events-none opacity-50">
											<Button
												:type="'primary'"
												:loading="showLoading"
												:show-x="showX"
												:message="t('callAthlete', numberAthletes)"
												@button-click="null" />
										</div>
									</Tooltip>
									<Button
										v-else
										:type="'primary'"
										:loading="showLoading"
										:show-x="showX"
										:message="t('callAthlete', numberAthletes)"
										@button-click="callRequest()" />
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
import RadioGroup from "@/components/partials/inputs/radioGroup.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import TextAreaInput from "@/components/partials/inputs/textAreaInput.vue";
import Button from "@/components/partials/button.vue";
import Tooltip from "@/components/partials/templates/tooltip.vue";
import { ArrowLeftCircleIcon, XCircleIcon } from "@heroicons/vue/24/outline";
import { useI18n } from "vue-i18n";
import { ref, watch, computed } from "vue";
import { authApi } from "@/services/api";
import toast from "@/toast.js";
import store from "@/store";
import { getAthleteNameTeam } from "@/services/athlete.service";

const props = defineProps({
	competitionId: {
		type: String,
		required: true,
	},
	open: {
		type: Boolean,
		required: true,
	},
	number: {
		type: Number,
		required: true,
	},
	morning: {
		type: Boolean,
		required: true,
	},
	day: {
		type: Number,
		required: true,
	},
});

let { t } = useI18n({ useScope: "global" });
let open = ref(props.open);
let showLoading = ref(false);
let showX = ref(false);
let match = ref(null);
let state = ref({
	number: 1,
	area: store.getters.getUser.name.split(" ")[1],
	callType: "c",
	callTypeOther: "",
	notes: "",
});

let numberAthletes = computed(
	() =>
		Number(match.value?.athlete_red_id !== null) + Number(match.value?.athlete_blue_id !== null)
);

const callTypes = [
	{
		value: "c",
		name: "callTypes.call",
	},
	{
		value: "s",
		name: "callTypes.second",
	},
	{
		value: "l",
		name: "callTypes.last",
	},
	{
		value: "p",
		name: "callTypes.prepare",
	},
	{
		value: "o",
		name: "callTypes.other",
	},
];
const emit = defineEmits(["close"]);

watch(
	() => props.open,
	(after) => {
		open.value = after;
		state.value.number = props.number;
		state.value.notes = "";
		state.value.callType = "c";
		state.value.callTypeOther = "";
		showLoading.value = false;
		showX.value = false;
		match.value = null;
	}
);

function callThis() {
	showLoading.value = true;
	showX.value = false;
	authApi
		.get(
			`matches/competitions/${props.competitionId}/call?area=${
				store.getters.getUser.name.split(" ")[1]
			}&day=${props.day}&morning=${props.morning.toString()}&number=${state.value.number}`
		)
		.then((response) => {
			match.value = response.data;
			showLoading.value = false;
		})
		.catch((error) => {
			showLoading.value = false;
			showX.value = true;
			toast.error(t("notFound.match"));
			console.error(error);
		});
}

function callRequest() {
	showLoading.value = true;
	showX.value = false;
	authApi
		.put(`matches/call-request/${match.value.id}`, {
			area_to_call: state.value.area,
			call_type:
				state.value.callType == "o" ? state.value.callTypeOther : state.value.callType,
			description_to_micro: state.value.notes,
		})
		.then(() => {
			match.value = null;
			showLoading.value = false;
			toast.success(t("success.call.sent"));
			emit("close");
		})
		.catch((error) => {
			showLoading.value = false;
			showX.value = true;
			toast.error(t("notFound.match"));
			console.error(error);
		});
}

function callSpecial(callTypeSpecial) {
	let objApi = null;
	if (callTypeSpecial == "f") {
		objApi = { call_request_fireman: true, area_to_call: state.value.area };
	} else {
		objApi = { call_request_clean: true, area_to_call: state.value.area };
	}
	authApi
		.put(
			`matches/special-request?competition_id=${props.competitionId}&area=${
				state.value.area
			}&day=${props.day}&morning=${props.morning.toString()}&number=${state.value.number}`,
			objApi
		)
		.then(() => {
			match.value = null;
			toast.success(t(`success.call.special.${callTypeSpecial}`));
			emit("close");
		})
		.catch((error) => {
			toast.error(t("notFound.match"));
			console.error(error);
		});
}
</script>
