<template>
	<div>
		<TransitionRoot as="template" :show="open">
			<Dialog as="div" class="fixed z-20 inset-0 overflow-y-auto">
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
							class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-show shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full sm:p-6">
							<Loading v-if="loading" :size="10" />
							<div v-else>
								<div class="inline-flex w-full">
									<p class="text-xl font-semibold text-center mb-4">
										{{ newAthlete ? t("new") : t("updateAt") }}
									</p>
									<div class="ml-auto">
										<XMarkIcon
											class="h-8 w-8 rounded-full border-2 border-gray-400 text-gray-600 hover:text-gray-900 cursor-pointer hover:bg-gray-300 hover:border-gray-600 active:bg-gray-500 active:border-gray-900 active:text-black"
											@click="emit('close')" />
									</div>
								</div>
								<form class="space-y-8 divide-y divide-gray-200">
									<div class="space-y-8 divide-y divide-gray-200 sm:space-y-5">
										<div class="space-y-6 sm:space-y-5">
											<!-- Title Athlete's Information -->
											<div>
												<h3
													class="text-lg font-medium leading-6 text-gray-900">
													{{ t("athletesT.information") }}
												</h3>
											</div>
											<div class="space-y-6 sm:space-y-5">
												<!-- Name and Birtday Input -->
												<div class="inline-flex w-full gap-x-8">
													<!-- Name Input -->
													<div class="w-2/3">
														<CustomInput
															type="text"
															:label="t('name')"
															:name="'name'"
															:readonly="searchedByFedNum"
															:option-selected="state.name"
															:error="
																v$.name.$errors.length == 0
																	? ''
																	: v$.name.$errors[0].$message
															"
															@value-changed="
																(option) => (state.name = option)
															" />
													</div>
													<!-- Birthday Input -->
													<div class="w-1/3">
														<DateInput
															:label="t('birthday')"
															:readonly="searchedByFedNum"
															:name="'birthday'"
															:option-selected="state.birthday"
															:error="
																v$.birthday.$errors.length == 0
																	? ''
																	: v$.birthday.$errors[0]
																			.$message
															"
															@value-changed="
																(option) =>
																	(state.birthday = option)
															" />
													</div>
												</div>

												<!-- Email Address and Phone Number Input -->
												<div class="inline-flex w-full gap-x-8">
													<!-- Email Address Input -->
													<div class="w-2/3">
														<CustomInput
															type="text"
															:label="t('email')"
															:name="'email'"
															:readonly="searchedByFedNum"
															:option-selected="state.email"
															:error="
																v$.email.$errors.length == 0
																	? ''
																	: v$.email.$errors[0].$message
															"
															@value-changed="
																(option) => (state.email = option)
															" />
													</div>
													<!-- Phone Number Input -->
													<div class="w-1/3">
														<CustomInput
															type="text"
															:label="t('phoneNumber')"
															:name="'phoneNumber'"
															:readonly="searchedByFedNum"
															:option-selected="state.phoneNumber"
															:error="
																v$.phoneNumber.$errors.length == 0
																	? ''
																	: v$.phoneNumber.$errors[0]
																			.$message
															"
															@value-changed="
																(option) =>
																	(state.phoneNumber = option)
															" />
													</div>
												</div>

												<!-- Nationality and Naturality Input -->
												<div class="inline-flex w-full gap-x-8">
													<!-- Nationality Input -->
													<div class="w-1/3">
														<SearchSelect
															:title="t('nationality')"
															:options="countries"
															:option-selected="state.nationality"
															:readonly="searchedByFedNum"
															:error="
																v$.nationality.$errors.length == 0
																	? ''
																	: v$.nationality.$errors[0]
																			.$message
															"
															@selected="
																(option) =>
																	(state.nationality = option)
															" />
													</div>
													<!-- Naturality Region Input -->
													<div class="w-1/3">
														<CustomInput
															type="text"
															:label="t('naturality.region')"
															:name="'naturalRegion'"
															:readonly="searchedByFedNum"
															:option-selected="state.naturalRegion"
															:error="
																v$.naturalRegion.$errors.length == 0
																	? ''
																	: v$.naturalRegion.$errors[0]
																			.$message
															"
															@value-changed="
																(option) =>
																	(state.naturalRegion = option)
															" />
													</div>
													<!-- Naturality Country Input -->
													<div class="w-1/3">
														<SearchSelect
															:title="t('naturality.country')"
															:options="countries"
															:option-selected="state.naturalCountry"
															:readonly="searchedByFedNum"
															:error="
																v$.naturalCountry.$errors.length ==
																0
																	? ''
																	: v$.naturalCountry.$errors[0]
																			.$message
															"
															@selected="
																(option) =>
																	(state.naturalCountry = option)
															" />
													</div>
												</div>

												<!-- Weight and Belt Input -->
												<div class="inline-flex w-full gap-x-8">
													<!-- Weight Input -->
													<div class="w-full">
														<CustomInput
															type="text"
															:label="t('weight')"
															:name="'weight'"
															:readonly="searchedByFedNum"
															:option-selected="state.weight"
															:error="
																v$.weight.$errors.length == 0
																	? ''
																	: v$.weight.$errors[0].$message
															"
															@value-changed="
																(option) => (state.weight = option)
															" />
													</div>

													<!-- Belt Input -->
													<div class="w-full">
														<SearchSelect
															:options="belts"
															:title="t('belt')"
															:option-selected="state.belt"
															:readonly="searchedByFedNum.value"
															:error="
																v$.belt.$errors.length == 0
																	? ''
																	: v$.belt.$errors[0].$message
															"
															@selected="
																(option) => (state.belt = option)
															" />
													</div>
												</div>

												<!-- Is Adapted, Gender and Competition Gender Input -->
												<div class="inline-flex w-full gap-x-8">
													<!-- Is Adapted Input -->
													<div class="w-1/3">
														<ToogleInput
															:label="t('isAdapted')"
															:name="'isAdapted'"
															:readonly="searchedByFedNum"
															:option-selected="state.isAdapted"
															:error="
																v$.isAdapted.$errors.length == 0
																	? ''
																	: v$.isAdapted.$errors[0]
																			.$message
															"
															@value-changed="
																(option) =>
																	(state.isAdapted = option)
															" />
													</div>
													<!-- Gender Input -->
													<div class="w-1/3">
														<RadioGroup
															:label="t('genderIsMale')"
															:name="'genderIsMale'"
															:readonly="searchedByFedNum"
															:option-selected="state.genderIsMale"
															:radio-options="[
																{ name: t('masc'), value: 'M' },
																{ name: t('fem'), value: 'F' },
																{
																	name: t('other'),
																	value: 'O',
																},
															]"
															:error="
																v$.genderIsMale.$errors.length == 0
																	? ''
																	: v$.genderIsMale.$errors[0]
																			.$message
															"
															@selected="
																(option) =>
																	(state.genderIsMale = option)
															" />
													</div>
													<!-- Competition Gender Input -->
													<div
														v-if="state.genderIsMale == 'O'"
														class="w-1/2">
														<RadioGroup
															:label="t('isMale')"
															:name="'isMale'"
															:readonly="searchedByFedNum"
															:option-selected="state.isMale"
															:radio-options="[
																{ name: t('masc'), value: 'M' },
																{ name: t('fem'), value: 'F' },
															]"
															:error="
																v$.isMale.$errors.length == 0
																	? ''
																	: v$.isMale.$errors[0].$message
															"
															@selected="
																(option) => (state.isMale = option)
															" />
													</div>
												</div>
											</div>

											<!-- Title Identification Documents -->
											<div class="sm:border-t sm:border-gray-200 sm:pt-5">
												<h3
													class="text-lg font-medium leading-6 text-gray-900">
													{{ t("athletesT.identificationDocuments") }}
												</h3>
											</div>
											<div class="space-y-6 sm:space-y-5">
												<!-- Identification Document Type Inputs -->
												<div class="inline-flex w-full gap-x-8">
													<!-- Identification Document Type Input -->
													<div class="w-1/2">
														<RadioGroup
															:label="
																t('identificationDocument.type')
															"
															:name="'identificationDocumentType'"
															:readonly="searchedByFedNum"
															:option-selected="
																state.identificationDocumentType
															"
															:columns="2"
															:radio-options="[
																{
																	name: t(
																		'identificationDocument.cc'
																	),
																	value: 'C',
																},
																{
																	name: t(
																		'identificationDocument.bi'
																	),
																	value: 'I',
																},
																{
																	name: t(
																		'identificationDocument.birthBulletin'
																	),
																	value: 'B',
																},
																{
																	name: t(
																		'identificationDocument.passport'
																	),
																	value: 'P',
																},
																{
																	name: t('other'),
																	value: 'O',
																},
															]"
															:error="
																v$.identificationDocumentType
																	.$errors.length == 0
																	? ''
																	: v$.identificationDocumentType
																			.$errors[0].$message
															"
															@selected="
																(option) =>
																	(state.identificationDocumentType =
																		option)
															" />
													</div>
													<!-- Other Identification Document -->
													<div
														v-if="
															state.identificationDocumentType == 'O'
														"
														class="w-1/2">
														<CustomInput
															type="text"
															:label="
																t(
																	'identificationDocument.otherType'
																)
															"
															:name="'otherIdentificationDocumentType'"
															:readonly="searchedByFedNum"
															:option-selected="
																state.otherIdentificationDocumentType
															"
															:error="
																v$.otherIdentificationDocumentType
																	.$errors.length == 0
																	? ''
																	: v$
																			.otherIdentificationDocumentType
																			.$errors[0].$message
															"
															@value-changed="
																(option) =>
																	(state.otherIdentificationDocumentType =
																		option)
															" />
													</div>
												</div>

												<!-- Identification Document Number, Emited By and Date Input -->
												<div class="inline-flex w-full gap-x-8">
													<!-- Identification Document Number Input -->
													<div class="w-full">
														<CustomInput
															type="text"
															:label="
																t('identificationDocument.number')
															"
															:name="'identificationDocumentNumber'"
															:readonly="searchedByFedNum"
															:option-selected="
																state.identificationDocumentNumber
															"
															:error="
																v$.identificationDocumentNumber
																	.$errors.length == 0
																	? ''
																	: v$
																			.identificationDocumentNumber
																			.$errors[0].$message
															"
															@value-changed="
																(option) =>
																	(state.identificationDocumentNumber =
																		option)
															" />
													</div>
													<!-- Identification Document Emited By Input -->
													<div
														v-if="
															state.identificationDocumentType != 'C'
														"
														class="w-full">
														<CustomInput
															type="text"
															:label="
																t('identificationDocument.emitedBy')
															"
															:name="'identificationDocumentEmitedBy'"
															:readonly="searchedByFedNum"
															:option-selected="
																state.identificationDocumentEmitedBy
															"
															:error="
																v$.identificationDocumentEmitedBy
																	.$errors.length == 0
																	? ''
																	: v$
																			.identificationDocumentEmitedBy
																			.$errors[0].$message
															"
															@value-changed="
																(option) =>
																	(state.identificationDocumentEmitedBy =
																		option)
															" />
													</div>
													<!-- Identification Document Date Input -->
													<div class="w-full">
														<DateInput
															:label="
																t('identificationDocument.date')
															"
															:readonly="searchedByFedNum"
															:name="'identificationDocumentExpirationDate'"
															:option-selected="
																state.identificationDocumentExpirationDate
															"
															:error="
																v$
																	.identificationDocumentExpirationDate
																	.$errors.length == 0
																	? ''
																	: v$
																			.identificationDocumentExpirationDate
																			.$errors[0].$message
															"
															@value-changed="
																(option) =>
																	(state.identificationDocumentExpirationDate =
																		option)
															" />
													</div>
												</div>

												<!-- NIF Input -->
												<div class="inline-flex w-full gap-x-8">
													<!-- NIF Input -->
													<div class="w-1/3">
														<CustomInput
															type="text"
															:label="t('nif')"
															:name="'nif'"
															:readonly="searchedByFedNum"
															:option-selected="state.nif"
															:error="
																v$.nif.$errors.length == 0
																	? ''
																	: v$.nif.$errors[0].$message
															"
															@value-changed="
																(option) => (state.nif = option)
															" />
													</div>
												</div>
											</div>

											<!-- Address Title -->
											<div class="sm:border-t sm:border-gray-200 sm:pt-5">
												<h3
													class="text-lg font-medium leading-6 text-gray-900">
													{{ t("athletesT.address") }}
												</h3>
											</div>
											<div class="space-y-6 sm:space-y-5">
												<!-- Address Input -->
												<div class="w-full">
													<TextAreaInput
														:rows="3"
														:label="t('address')"
														:name="'address'"
														:readonly="searchedByFedNum"
														:option-selected="state.address"
														:error="
															v$.address.$errors.length == 0
																? ''
																: v$.address.$errors[0].$message
														"
														@value-changed="
															(option) => (state.address = option)
														" />
												</div>

												<!-- Region and Zip Code Input -->
												<div class="inline-flex w-full gap-x-8">
													<!-- Region Input -->
													<div class="w-2/3">
														<CustomInput
															type="text"
															:label="t('region')"
															:name="'region'"
															:readonly="searchedByFedNum"
															:option-selected="state.region"
															:error="
																v$.region.$errors.length == 0
																	? ''
																	: v$.region.$errors[0].$message
															"
															@value-changed="
																(option) => (state.region = option)
															" />
													</div>
													<!-- Zip Code Input -->
													<div class="w-1/3">
														<CustomInput
															type="text"
															:label="t('zipCode')"
															:name="'zipCode'"
															:mask="'####-###'"
															:readonly="searchedByFedNum"
															:option-selected="state.zipCode"
															:error="
																v$.zipCode.$errors.length == 0
																	? ''
																	: v$.zipCode.$errors[0].$message
															"
															@value-changed="
																(option) => (state.zipCode = option)
															" />
													</div>
												</div>
												<!-- Country Input -->
												<div class="w-full">
													<SearchSelect
														:title="t('country')"
														:options="countries"
														:option-selected="state.country"
														:error="
															v$.country.$errors.length == 0
																? ''
																: v$.country.$errors[0].$message
														"
														@selected="
															(option) => (state.country = option)
														" />
												</div>
											</div>

											<!-- Athlete's Responsible Title -->
											<div
												v-if="showResponsible"
												class="sm:border-t sm:border-gray-200 sm:pt-5">
												<h3
													class="text-lg font-medium leading-6 text-gray-900">
													{{ t("athletesT.responsible") }}
												</h3>
											</div>
											<div
												v-if="showResponsible"
												class="space-y-6 sm:space-y-5">
												<!-- Athlete's Responsible Name and Relationship Input -->
												<div class="inline-flex w-full gap-x-8">
													<div class="w-full">
														<CustomInput
															type="text"
															:label="t('responsible.name')"
															:name="'responsibleName'"
															:readonly="searchedByFedNum"
															:option-selected="state.responsibleName"
															:error="
																v$.responsibleName.$errors.length ==
																0
																	? ''
																	: v$.responsibleName.$errors[0]
																			.$message
															"
															@value-changed="
																(option) =>
																	(state.responsibleName = option)
															" />
													</div>

													<!-- Athlete's Responsible Relationship Input -->
													<div class="w-1/2">
														<CustomInput
															type="text"
															:label="t('responsible.relationship')"
															:name="'responsibleRelationship'"
															:readonly="searchedByFedNum"
															:option-selected="
																state.responsibleRelationship
															"
															:error="
																v$.responsibleRelationship.$errors
																	.length == 0
																	? ''
																	: v$.responsibleRelationship
																			.$errors[0].$message
															"
															@value-changed="
																(option) =>
																	(state.responsibleRelationship =
																		option)
															" />
													</div>
												</div>

												<!-- Athlete's Responsible Email Input -->
												<div class="inline-flex w-full gap-x-8">
													<CustomInput
														type="text"
														:label="t('responsible.email')"
														:name="'responsibleEmail'"
														:readonly="searchedByFedNum"
														:option-selected="state.responsibleEmail"
														:error="
															v$.responsibleEmail.$errors.length == 0
																? ''
																: v$.responsibleEmail.$errors[0]
																		.$message
														"
														@value-changed="
															(option) =>
																(state.responsibleEmail = option)
														" />
												</div>

												<!-- Athlete's Responsible Identification Document Number and Identification Document Expiration Date Input -->
												<div class="inline-flex w-full gap-x-8">
													<!-- Athlete's Responsible Identification Document Number Input -->
													<div class="w-full">
														<CustomInput
															type="text"
															:label="
																t(
																	'responsible.identificationDocumentNumber'
																)
															"
															:name="'responsibleIdentificationDocumentNumber'"
															:readonly="searchedByFedNum"
															:option-selected="
																state.responsibleIdentificationDocumentNumber
															"
															:error="
																v$
																	.responsibleIdentificationDocumentNumber
																	.$errors.length == 0
																	? ''
																	: v$
																			.responsibleIdentificationDocumentNumber
																			.$errors[0].$message
															"
															@value-changed="
																(option) =>
																	(state.responsibleIdentificationDocumentNumber =
																		option)
															" />
													</div>
													<!-- Athlete's Responsible Identification Document Expiration Date Input -->
													<div class="w-full">
														<DateInput
															:label="
																t(
																	'responsible.identificationDocumentExpirationDate'
																)
															"
															:readonly="searchedByFedNum"
															:name="'responsibleIdentificationDocumentExpirationDate'"
															:option-selected="
																state.responsibleIdentificationDocumentExpirationDate
															"
															:error="
																v$
																	.responsibleIdentificationDocumentExpirationDate
																	.$errors.length == 0
																	? ''
																	: v$
																			.responsibleIdentificationDocumentExpirationDate
																			.$errors[0].$message
															"
															@value-changed="
																(option) =>
																	(state.responsibleIdentificationDocumentExpirationDate =
																		option)
															" />
													</div>
												</div>
											</div>
										</div>
									</div>
								</form>
								<div class="relative w-60 left-1/2 -translate-x-1/2 mt-20">
									<Button
										:loading="showSpinningWheel"
										:show-x="showX"
										:show-check="showCheck"
										:message="newAthlete ? t('create') : t('update')"
										type="primary"
										@button-click="createAthlete" />
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
import Loading from "@/components/partials/loading.vue";
import DateInput from "@/components/partials/inputs/dateInput.vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import TextAreaInput from "@/components/partials/inputs/textAreaInput.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import ToogleInput from "@/components/partials/inputs/toogle.vue";
import RadioGroup from "@/components/partials/inputs/radioGroup.vue";
import Button from "@/components/partials/button.vue";
import { XMarkIcon } from "@heroicons/vue/24/solid";
import { Dialog, DialogOverlay, TransitionChild, TransitionRoot } from "@headlessui/vue";
import { ref, watch, computed } from "vue";
import { authApi, errorHandling } from "@/services/api";
import { required, helpers, numeric } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import toast, { genericError } from "@/toast.js";
import { useI18n } from "vue-i18n";
import c from "country-list";
import e from "countries-list";

let { t, locale } = useI18n({ useScope: "global" });

const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	teamId: {
		type: String,
		required: true,
	},
	athleteId: {
		type: String,
		required: false,
		default: "",
	},
});
const emit = defineEmits(["close", "created", "updated"]);

const req = helpers.withMessage(t("errors.required"), required);
const competitionGenderReq = helpers.withMessage(t("errors.required"), (value) =>
	state.value.isMale == "O" ? value.includes("M") || value.includes("F") : true
);
const num = helpers.withMessage(t("errors.numeric"), numeric);

let state = ref({
	number: "",
	name: "",
	email: "",
	birthday: "",
	phoneNumber: "",
	genderIsMale: "",
	isMale: "",
	nationality: "",
	naturalRegion: "",
	naturalCountry: "",
	identificationDocumentType: "",
	otherIdentificationDocumentType: "",
	identificationDocumentNumber: "",
	identificationDocumentExpirationDate: "",
	identificationDocumentEmitedBy: "",
	responsibleName: "",
	responsibleIdentificationDocumentNumber: "",
	responsibleRelationship: "",
	responsibleEmail: "",
	responsibleIdentificationDocumentExpirationDate: "",
	address: "",
	nif: "",
	region: "",
	zipCode: "",
	country: "",
	weight: "",
	belt: "",
	isAdapted: false,
});

let rules = {
	number: {},
	name: {
		req: req,
	},
	birthday: {
		req: req,
	},
	genderIsMale: {
		req: req,
	},
	weight: {
		req: req,
		num: num,
	},
	belt: {
		req: req,
	},
	isMale: {
		req: competitionGenderReq,
	},
	email: {},
	phoneNumber: {},
	nationality: {},
	naturalRegion: {},
	naturalCountry: {},
	identificationDocumentType: {},
	otherIdentificationDocumentType: {},
	identificationDocumentNumber: {},
	identificationDocumentExpirationDate: {},
	identificationDocumentEmitedBy: {},
	responsibleName: {},
	responsibleIdentificationDocumentNumber: {},
	responsibleRelationship: {},
	responsibleEmail: {},
	responsibleIdentificationDocumentExpirationDate: {},
	address: {},
	nif: {},
	region: {},
	zipCode: {},
	country: {},
	isAdapted: {},
};

let v$ = useVuelidate(rules, state);
let open = ref(props.open);
let showSpinningWheel = ref(false);
let loading = ref(!true);
let showCheck = ref(false);
let showX = ref(false);
let newAthlete = ref(true);
let searchedByFedNum = ref(false);
let federationNumberError = ref("");
let belts = ref([]);
let todayDate = new Date();

let showResponsible = computed(() => {
	if (state.value.birthday == null || state.value.birthday == "") return true;
	if (typeof state.value.birthday == "string") {
		return Number(state.value.birthday.split("-")[2]) + 18 > todayDate.getFullYear();
	}
	return state.value.birthday.getFullYear() + 18 > todayDate.getFullYear();
});
let n = c.getCodeList();
let keys = Object.keys(n);
let countries = ref([]);
keys.forEach((key) => {
	countries.value.push({
		id: key.toUpperCase(),
		name: e.getEmojiFlag(key.toUpperCase()) + " " + n[key],
	});
});
let allBelts = ref([]);
let control = ref(true);
authApi
	.get("belts")
	.then((response) => {
		allBelts.value = response.data;
		for (let belt of response.data) {
			belts.value.push({ name: t(`belts.${belt.name}`), id: belt.id });
		}
	})
	.catch(() => {
		genericError();
		emit("close");
	});

watch(
	() => state.value.weight,
	(after) => {
		if (control.value) {
			state.value.weight = after.replace(",", ".");
			control.value = false;
		}
		control.value = true;
	}
);
watch(
	() => locale.value,
	() => {
		belts.value = [];
		for (let belt of allBelts.value) {
			belts.value.push({ name: t(`belts.${belt.name}`), id: belt.id });
		}
	}
);
watch(
	() => props.open,
	(after) => {
		open.value = after;
		if (after) {
			loading.value = true;
			newAthlete.value = props.athleteId == "";
			showCheck.value = false;
			showX.value = false;
			showSpinningWheel.value = false;
			setAthlete(null);
			v$.value.$reset();
			if (!newAthlete.value) {
				authApi
					.get(`athletes/${props.athleteId}`)
					.then((response) => {
						if (response.data == null) {
							toast.error("erros.athlete");
							emit("close");
							return;
						}
						setAthlete(response.data);
						loading.value = false;
					})
					.catch(() => {
						toast.error("erros.athlete");
						emit("close");
					});
			} else {
				loading.value = false;
			}
		}
	}
);

function setAthlete(apiData) {
	let birthdayAux = "";
	if (apiData?.birthday != null) {
		let aux = apiData.birthday.split("T")[0].split("-");
		birthdayAux = `${aux[2]}-${aux[1]}-${aux[0]}`;
	}
	state.value.birthday = birthdayAux;
	let identificationDocumentExpirationDateAux = "";
	if (apiData?.identification_document_expiration_date != null) {
		let aux = apiData.identification_document_expiration_date.split("T")[0].split("-");
		identificationDocumentExpirationDateAux = `${aux[2]}-${aux[1]}-${aux[0]}`;
	} else if (apiData?.identificationDocumentExpirationDate != null) {
		let aux = apiData.identificationDocumentExpirationDate.split("T")[0].split("-");
		identificationDocumentExpirationDateAux = `${aux[2]}-${aux[1]}-${aux[0]}`;
	}
	state.value.identificationDocumentExpirationDate = identificationDocumentExpirationDateAux;
	let responsibleIdentificationDocumentExpirationDateAux = "";
	if (apiData?.responsible_identification_document_expiration_date != null) {
		let aux = apiData.responsible_identification_document_expiration_date
			.split("T")[0]
			.split("-");
		responsibleIdentificationDocumentExpirationDateAux = `${aux[2]}-${aux[1]}-${aux[0]}`;
	} else if (apiData?.responsibleIdentificationDocumentExpirationDate != null) {
		let aux = apiData.responsibleIdentificationDocumentExpirationDate.split("T")[0].split("-");
		identificationDocumentExpirationDateAux = `${aux[2]}-${aux[1]}-${aux[0]}`;
	}
	state.value.responsibleIdentificationDocumentExpirationDateAux =
		responsibleIdentificationDocumentExpirationDateAux;
	state.value.name = apiData?.name != null ? apiData.name : "";
	state.value.email = apiData?.email != null ? apiData.email : "";
	state.value.phoneNumber =
		apiData?.phone_number != null
			? apiData.phone_number
			: apiData?.phoneNumber != null
			? apiData.phoneNumber
			: "";
	state.value.genderIsMale =
		apiData?.gender_is_male != null
			? apiData.gender_is_male
			: apiData?.genderIsMale != null
			? apiData.genderIsMale
			: "";
	state.value.isMale =
		apiData?.is_male != null
			? apiData?.is_male
				? "M"
				: "F"
			: apiData?.isMale != null
			? apiData.isMale
			: "";
	state.value.nationality = apiData?.nationality != null ? apiData.nationality : "";
	state.value.naturalRegion =
		apiData?.natural_region != null
			? apiData.natural_region
			: apiData?.naturalRegion != null
			? apiData.naturalRegion
			: "";
	state.value.naturalCountry =
		apiData?.natural_country != null
			? apiData.natural_country
			: apiData?.naturalCountry != null
			? apiData.naturalCountry
			: "";
	let identificationTypes = ["C", "B", "I", "P"];
	if (apiData?.identification_document_type != null) {
		if (identificationTypes.indexOf(apiData.identification_document_type) != -1) {
			state.value.identificationDocumentType = apiData.identification_document_type;
			state.value.otherIdentificationDocumentType = "";
		} else {
			state.value.identificationDocumentType = "O";
			state.value.otherIdentificationDocumentType = apiData.identification_document_type;
		}
	} else if (apiData?.identificationDocumentType != null) {
		if (identificationTypes.indexOf(apiData.identificationDocumentType) != -1) {
			state.value.identificationDocumentType = apiData.identificationDocumentType;
			state.value.otherIdentificationDocumentType = "";
		} else {
			state.value.identificationDocumentType = "O";
			state.value.otherIdentificationDocumentType = apiData.identificationDocumentType;
		}
	} else {
		state.value.identificationDocumentType = "";
		state.value.otherIdentificationDocumentType = "";
	}
	state.value.naturalRegion =
		apiData?.natural_region != null
			? apiData.natural_region
			: apiData?.naturalRegion != null
			? apiData.naturalRegion
			: "";
	state.value.naturalCountry =
		apiData?.natural_country != null
			? apiData.natural_country
			: apiData?.naturalCountry != null
			? apiData.naturalCountry
			: "";
	state.value.identificationDocumentNumber =
		apiData?.identification_document_number != null
			? apiData.identification_document_number
			: apiData?.identificationDocumentNumber != null
			? apiData.identificationDocumentNumber
			: "";
	state.value.identificationDocumentEmitedBy =
		apiData?.identification_document_emitted_by != null
			? apiData.identification_document_emitted_by
			: apiData?.identificationDocumentEmitedBy != null
			? apiData.identificationDocumentEmitedBy
			: "";
	state.value.responsibleName =
		apiData?.responsible_name != null
			? apiData.responsible_name
			: apiData?.responsibleName != null
			? apiData.responsibleName
			: "";
	state.value.responsibleIdentificationDocumentNumber =
		apiData?.responsible_identification_document_number != null
			? apiData.responsible_identification_document_number
			: apiData?.responsibleIdentificationDocumentNumber != null
			? apiData.responsibleIdentificationDocumentNumber
			: "";
	state.value.responsibleRelationship =
		apiData?.responsible_relationship != null
			? apiData.responsible_relationship
			: apiData?.responsibleRelationship != null
			? apiData.responsibleRelationship
			: "";
	state.value.responsibleEmail =
		apiData?.responsible_email != null
			? apiData.responsible_email
			: apiData?.responsibleEmail != null
			? apiData.responsibleEmail
			: "";
	state.value.nif = apiData?.nif != null ? apiData.nif : "";
	state.value.address = apiData?.address != null ? apiData.address : "";
	state.value.region = apiData?.region != null ? apiData.region : "";
	state.value.zipCode =
		apiData?.zip_code != null
			? apiData.zip_code
			: apiData?.zipCode != null
			? apiData?.zipCode
			: "";
	state.value.country = apiData?.country != null ? apiData.country : "";
	state.value.weight = apiData?.weight != null ? apiData.weight.toString() : "";
	state.value.belt =
		apiData?.belt_id != null
			? apiData.belt_id
			: apiData?.beltId != null
			? apiData.beltId
			: apiData?.belt != null
			? apiData.belt.id != null
				? apiData.belt.id
				: apiData.belt
			: "";
	state.value.isAdapted =
		apiData?.is_adapted != null
			? apiData.is_adapted
			: apiData?.isAdapted != null
			? apiData.isAdapted
			: false;
	state.value.number =
		apiData?.federation_number != null
			? apiData.federation_number
			: apiData?.number != null
			? apiData.number
			: "";
}

function searchFed() {
	authApi
		.get(`athletes/number/${state.value.number}`)
		.then((response) => {
			setAthlete(response.data);
			if (response.data == null) {
				federationNumberError.value = t("errors.fed");
				return;
			}
			searchedByFedNum.value = true;
		})
		.catch(() => {
			searchedByFedNum.value = false;
			setAthlete(null);
			federationNumberError.value = t("errors.fed");
		});
}

async function createAthlete() {
	showX.value = false;
	showCheck.value = false;
	showSpinningWheel.value = true;

	let isFormValid = await v$.value.$validate();
	if (!isFormValid) {
		showX.value = true;
		showSpinningWheel.value = false;
		return;
	}
	let athleteToCreate = {
		name: state.value.name,
		is_male:
			state.value.genderIsMale == "O"
				? state.value.isMale == "M"
				: state.value.genderIsMale == "M",
		weight: state.value.weight.replace(",", "."),
		email: state.value.email,
		phone_number: state.value.phoneNumber,
		nationality: state.value.nationality,
		natural_region: state.value.naturalRegion,
		natural_country: state.value.naturalCountry,
		gender_is_male: state.value.genderIsMale,
		identification_document_type:
			state.value.identificationDocumentType == "O"
				? state.value.otherIdentificationDocumentType
				: state.value.identificationDocumentType,
		identification_document_number: state.value.identificationDocumentNumber,
		identification_document_emitted_by: state.value.identificationDocumentEmitedBy,
		identification_document_expiration_date: state.value.identificationDocumentExpirationDate,
		responsible_name: state.value.responsibleName,
		responsible_identification_document_number:
			state.value.responsibleIdentificationDocumentNumber,
		responsible_identification_document_expiration_date:
			state.value.responsibleIdentificationDocumentExpirationDate,
		responsible_relationship: state.value.responsibleRelationship,
		responsible_email: state.value.responsibleEmail,
		nif: state.value.nif,
		address: state.value.address,
		zip_code: state.value.zipCode,
		region: state.value.region,
		country: state.value.country,
		is_adapted: state.value.isAdapted,
		belt_id: state.value.belt,
		team_id: props.teamId,
		birthday: state.value.birthday,
	};
	let promisse = newAthlete.value
		? authApi.post("athletes", athleteToCreate)
		: authApi.put(`athletes/${props.athleteId}`, athleteToCreate);
	promisse
		.then(() => {
			showSpinningWheel.value = false;
			showCheck.value = true;
			if (newAthlete.value) {
				emit("created");
			} else {
				emit("updated");
			}
			emit("close");
		})
		.catch((error) => {
			errorHandling(error);
			showSpinningWheel.value = false;
			showX.value = true;
			toast.error(newAthlete.value ? t("errors.create") : t("errors.update"));
		});
}
</script>

<i18n>
{
	"en_GB": {
		"nif": "NIF",
		"isAdapted": "Adapted",
		"masc": "Masculine",
		"fem": "Feminine",
		"other": "Other",
		"name": "Name*",
		"email": "Email Address",
		"genderIsMale": "Gender*",
		"isMale": "Competition Gender",
		"birthday": "Birthday*",
		"address": "Address",
		"zipCode": "Zip Code",
		"region": "Region",
		"country": "Country",
		"phoneNumber": "Phone Number",
		"weight": "Weight (Kg.)*",
		"belt": "Belt*",
		"new": "New Atlhete",
		"updateAt": "Update Atlhete",
		"create": "Create",
		"update": "Update",
		"fedNumber": "Federation Number",
		"addFed": "Search",
		"nationality": "Nationality",
		"naturality": {
			"region": "Natural of the Region",
			"country": "Natural of the Country"
		},
		"athletesT":  {
			"information": "Athlete's Information",
			"identificationDocuments": "Athlete's Identification Documents",
			"address": "Athlete's Address",
			"responsible": "Athlete's Responsible"
		},
		"identificationDocument": {
			"type": "Document Type",
			"otherType": "Other Document Type",
			"cc": "Citzen Card",
			"bi": "Identity Card",
			"birthBulletin": "Birth Bulletin",
			"passport": "Passport",
			"number": "Document Number",
			"date": "Date",
			"emitedBy": "Emited By",
		},
		"responsible": {
			"name": "Name",
			"email": "Email",
			"relationship": "Relationship",
			"identificationDocumentNumber": "Identification Document Number",
			"identificationDocumentExpirationDate": "Expiration Date",
		},
		"errors": {
			"athlete": "It wasn't possible to load the atlhete",
			"fed": "There isn't an athelete with this number",
			"create": "It wasn't possible to create the athlete",
			"update": "It wasn't possible to update the athlete",
			"required": "Cannot be empty",
			"maxLen": "The max length is {count} characters",
			"numeric": "Must be a number"
		},
		"belts": {
			"white": "White",
			"white-yellow": "White and Yellow",
			"yellow": "Yellow",
			"yellow-orange": "Yellow and Orange",
			"orange": "Orange",
			"orange-purple": "Orange and Purple",
			"purple": "Purple",
			"purple-blue": "Purple and Blue",
			"blue": "Blue",
			"blue-green": "Blue and Green",
			"green": "Green",
			"brown-jr": "Brown Junior",
			"brown": "Brown",
			"black-jr": "Black Junior",
			"black": "Black",
			"duan-1": "Duan 1",
			"duan-2": "Duan 2",
			"duan-3": "Duan 3+",
		},
	},
	"pt_PT": {
		"nif": "NIF",
		"isAdapted": "Adaptado",
		"masc": "Masculino",
		"fem": "Feminino",
		"other": "Outro",
		"name": "Nome*",
		"email": "Endereço de Email",
		"genderIsMale": "Género*",
		"isMale": "Género na Competição",
		"birthday": "Data de nascimento*",
		"address": "Morada",
		"zipCode": "Código Postal",
		"region": "Cidade/Localidade",
		"country": "País",
		"phoneNumber": "Número de telemóvel",
		"weight": "Peso (Kg.)*",
		"belt": "Cinto*",
		"new": "Novo Atleta",
		"updateAt": "Atualizar Atleta",
		"create": "Criar",
		"update": "Atualizar",
		"fedNumber": "Número de Federado",
		"addFed": "Pesquisar",
		"nationality": "Nacionalidade",
		"naturality": {
			"region": "Natural do Concelho de",
			"country": "Natural do País de"
		},
		"athletesT":  {
			"information": "Informação do Atleta",
			"identificationDocuments": "Documentos de Identificação do Atleta",
			"address": "Endereço do Atleta",
			"responsible": "Encarregado de Educação do Atleta"
		},
		"identificationDocument": {
			"type": "Tipo de Documento",
			"otherType": "Outro Tipo de Documento",
			"cc": "Cartão de Cidadão",
			"bi": "Bilhete de Identidade",
			"birthBulletin": "Cédula/Boletim de Nascimento",
			"passport": "Passaporte",
			"emitedBy": "Emitido Por",
			"number": "Número do Documento",
			"date": "Data",
		},
		"responsible": {
			"name": "Nome",
			"email": "Email",
			"relationship": "Parentesco",
			"identificationDocumentNumber": "Número do Cartão de Identificação",
			"identificationDocumentExpirationDate": "Data de Validade",
		},
		"errors": {
			"athlete": "Não foi possível carregar o atleta",
			"fed": "Não existe um atleta com este número de federado",
			"create": "Não foi possível criar o atleta",
			"update": "Não foi possível atualizar o atleta",
			"required": "Não pode estar vazio",
			"maxLen": "O comprimento máximo é de {count} caracteres",
			"numeric": "Tem de ser um número"
		},
		"belts": {
			"white": "Branco",
			"white-yellow": "Branco e Amarelo",
			"yellow": "Amarelo",
			"yellow-orange": "Amarelo e Laranja",
			"orange": "Laranja",
			"orange-purple": "Laranja e Púrpura",
			"purple": "Púrpura",
			"purple-blue": "Púrpura e Azul",
			"blue": "Azul",
			"blue-green": "Azul e Verde",
			"green": "Verde",
			"brown-jr": "Castanho Junior",
			"brown": "Castanho",
			"black-jr": "Preto Junior",
			"black": "Preto",
			"duan-1": "Duan 1",
			"duan-2": "Duan 2",
			"duan-3": "Duan 3+",
		},
	},
}
</i18n>
