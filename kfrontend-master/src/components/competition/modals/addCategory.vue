<template>
	<Modal :open="props.open" :outside-click="false" :show-x="true" @close="emit('close')">
		<div>
			<p class="mx-auto w-full text-xl font-semibold text-center -mt-8">
				{{ t("addCategory") }}
			</p>
			<Loading v-if="loading" :size="10" />
			<div v-else>
				<!-- Create or update category -->
				<div v-if="newCategory || editCategory">
					<Button
						class="max-w-max mb-2"
						:message="t('returnToCategorytList')"
						:icon-left="true"
						:icon="ArrowLeftIcon"
						:type="'black'"
						:size="'small'"
						@button-click="closeCategory" />

					<!-- Category form -->
					<div class="w-full space-y-8 flex flex-col">
						<CustomInput
							:label="t('name')"
							type="text"
							:name="'name'"
							:option-selected="state.name"
							:error="v$.name.$errors.length === 0 ? '' : v$.name.$errors[0].$message"
							@value-changed="(option) => (state.name = option)" />
						<SearchSelect
							:title="t('forms.type')"
							:option-selected="state.type"
							:options="categoriesTypes"
							:error="''"
							@selected="(option) => (state.type = option)" />
						<div class="inline-flex">
							<ToogleInput
								:label="t('forms.thirdPlaceDispute')"
								:sub-label="''"
								:option-selected="state.thirdPlace"
								@value-changed="(option) => (state.thirdPlace = option)" />
							<div class="ml-1 -mt-1">
								<Help :message="t('tooltips.thirdPlaceDispute')" />
							</div>
						</div>
						<div class="inline-flex">
							<ToogleInput
								:label="t('forms.singlePointOrThreePoints')"
								:sub-label="''"
								:option-selected="state.threePoints"
								@value-changed="(option) => (state.threePoints = option)" />
							<div class="ml-1 -mt-1">
								<Help :message="t('tooltips.singlePointOrThreePoints')" />
							</div>
						</div>
						<div class="inline-flex">
							<ToogleInput
								:label="t('forms.hasRounds')"
								:sub-label="''"
								:option-selected="state.rounds"
								@value-changed="(option) => (state.rounds = option)" />
							<div class="ml-1 -mt-1">
								<Help :message="t('tooltips.hasRounds')" />
							</div>
						</div>
						<div class="inline-flex">
							<ToogleInput
								:label="t('forms.hasPenalties')"
								:sub-label="''"
								:option-selected="state.penalties"
								@value-changed="(option) => (state.penalties = option)" />
							<div class="ml-1 -mt-1">
								<Help :message="t('tooltips.hasPenalties')" />
							</div>
						</div>
						<div class="inline-flex">
							<ToogleInput
								:label="t('forms.numberAllMatchesAtOnce')"
								:sub-label="''"
								:option-selected="state.numberAllAtOnce"
								@value-changed="(option) => (state.numberAllAtOnce = option)" />
							<div class="ml-1 -mt-1">
								<Help :message="t('tooltips.numberAllMatchesAtOnce')" />
							</div>
						</div>
						<div class="inline-flex">
							<ToogleInput
								:label="t('forms.teamCategory')"
								:sub-label="''"
								:option-selected="state.teamCategory"
								@value-changed="(option) => (state.teamCategory = option)" />
							<div class="ml-1 -mt-1">
								<Help :message="t('tooltips.teamCategory')" />
							</div>
						</div>
						<CustomInput
							v-if="state.teamCategory"
							:label="t('numberOfAthletesInTheTeam')"
							type="text"
							:name="'teamNumber'"
							:mask="'###'"
							:option-selected="state.teamNumber.toString()"
							@value-changed="(option) => (state.teamNumber = option)" />
					</div>

					<div class="relative w-60 left-1/2 -translate-x-1/2 mt-8">
						<Button
							:loading="showSpinningWheel"
							:show-x="showX"
							:show-check="showCheck"
							:message="newCategory ? t('createCategory') : t('updateCategory')"
							type="primary"
							@button-click="createOrUpdateCategory" />
					</div>
				</div>

				<!-- Set categories separations (sex, age, etc..) and price -->
				<div v-else-if="confirm">
					<!-- Title and return button -->
					<div class="inline-flex w-full justify-between">
						<p class="text-xl text-left font-semibold">
							{{ categoryToConfirm.name }}
						</p>
						<Button
							class="max-w-max mb-2"
							:message="t('returnToCategorytList')"
							:icon-left="true"
							:icon="ArrowLeftIcon"
							:type="'black'"
							:size="'small'"
							@button-click="
								categoryToConfirm = null;
								confirm = false;
							" />
					</div>

					<div class="w-full grid grid-cols-3 gap-x-4">
						<!-- Price and separations form and import select -->
						<div class="flex flex-col space-y-4">
							<CustomInput
								:label="t('forms.inscriptionPrice')"
								type="text"
								:name="'price'"
								:option-selected="categoryPrice.toString()"
								:error="''"
								@value-changed="(option) => (categoryPrice = option)" />
							<ToogleInput
								:label="t('forms.separateBySex')"
								:option-selected="stateConfirm.separateSex"
								@value-changed="(option) => (stateConfirm.separateSex = option)" />
							<ToogleInput
								:label="t('forms.separateByAge')"
								:option-selected="stateConfirm.separateAge"
								@value-changed="(option) => (stateConfirm.separateAge = option)" />
							<ToogleInput
								:label="t('forms.separateByWeight')"
								:option-selected="stateConfirm.separateWeight"
								@value-changed="
									(option) => (stateConfirm.separateWeight = option)
								" />
							<ToogleInput
								:label="t('forms.separateByBelt')"
								:option-selected="stateConfirm.separateBelt"
								@value-changed="(option) => (stateConfirm.separateBelt = option)" />

							<SearchSelect
								:title="t('importFromCategory')"
								:option-selected="categoryToUseDefault"
								:options="categoriesDefaults"
								:error="categoryImportError ? t('error.required') : ''"
								@selected="
									(option) => {
										categoryToUseDefault = option;
										categoryImportError = false;
									}
								" />
							<Button
								:message="t('importSeparations')"
								type="secondary"
								:loading="showSpinningWheelImport"
								@button-click="getSeparationsFromOtherCategory" />
						</div>

						<!-- Form separate by ages -->
						<div
							v-if="stateConfirm.separateAge"
							:class="[
								'grid col-span-2',
								stateConfirm.separateSex ? 'grid-cols-2 gap-x-6' : 'grid-cols-1',
							]">
							<p class="text-center col-span-full mb-2 text-lg">
								{{ t("forms.separateByAge") }}
							</p>
							<div>
								<p v-if="stateConfirm.separateSex" class="text-center">
									{{ t("masc") }}
								</p>
								<div v-for="age of ageMasc" :key="age" class="grid grid-cols-2">
									<input
										v-model="age.min"
										v-mask="'##'"
										type="text"
										class="appearance-none border-none bg-gray-100 rounded-lg m-1 text-center" />
									<input
										v-model="age.max"
										v-mask="'##'"
										type="text"
										class="appearance-none border-none bg-gray-100 rounded-lg m-1 text-center" />
								</div>
								<div class="grid grid-cols-2 m-1 gap-x-2">
									<div
										class="text-green-800 bg-green-500 w-full rounded-lg px-1 py-2 cursor-pointer hover:bg-green-400"
										@click="
											ageMasc.push({
												min: '',
												max: '',
											})
										">
										<PlusIcon class="h-5 w-5 m-auto" />
									</div>
									<div
										class="text-red-800 bg-red-500 w-full rounded-lg px-1 py-2 cursor-pointer hover:bg-red-400"
										@click="ageMasc.pop()">
										<MinusIcon class="h-5 w-5 m-auto" />
									</div>
								</div>
							</div>
							<div v-if="stateConfirm.separateSex">
								<p class="text-center">
									{{ t("fem") }}
								</p>
								<div v-for="age of ageFem" :key="age" class="grid grid-cols-2">
									<input
										v-model="age.min"
										v-mask="'##'"
										type="text"
										class="appearance-none border-none bg-gray-100 rounded-lg m-1 text-center" />
									<input
										v-model="age.max"
										v-mask="'##'"
										type="text"
										class="appearance-none border-none bg-gray-100 rounded-lg m-1 text-center" />
								</div>
								<div class="grid grid-cols-2 m-1 gap-x-2">
									<div
										class="text-green-800 bg-green-500 w-full rounded-lg px-1 py-2 cursor-pointer hover:bg-green-400"
										@click="
											ageFem.push({
												min: '',
												max: '',
											})
										">
										<PlusIcon class="h-5 w-5 m-auto" />
									</div>
									<div
										class="text-red-800 bg-red-500 w-full rounded-lg px-1 py-2 cursor-pointer hover:bg-red-400"
										@click="ageFem.pop()">
										<MinusIcon class="h-5 w-5 m-auto" />
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- Continue button -->
					<Button
						class="mt-20"
						:loading="showSpinningWheel"
						:show-x="showX"
						:show-check="showCheck"
						:message="
							stateConfirm.separateWeight
								? t('setWeightLimits')
								: stateConfirm.separateBelt
								? t('setBeltsRange')
								: t('createTournamentsForThisCategory')
						"
						type="primary"
						@button-click="
							() => {
								if (stateConfirm.separateWeight) verifyAges();
								else if (stateConfirm.separateBelt) prepareBelts();
								else createTourns();
							}
						" />
				</div>

				<!-- Set weights separations -->
				<div v-else-if="setWeights">
					<!-- Title and return button -->
					<div class="inline-flex w-full justify-between">
						<p class="text-xl text-left font-semibold">
							{{ categoryToConfirm.name }}
						</p>
						<Button
							class="max-w-max mb-2"
							:message="t('returnToDefineAges')"
							:icon-left="true"
							:icon="ArrowLeftIcon"
							:type="'black'"
							:size="'small'"
							@button-click="
								setWeights = false;
								confirm = true;
							" />
					</div>

					<div class="w-72">
						<!-- Age/sex separation selection -->
						<select
							id="weightSelect"
							v-model="weightSeparation"
							name="weightSelect"
							class="w-full text-center">
							<option
								v-for="separation in Object.keys(weightSeparations)"
								:key="separation"
								:value="separation">
								{{ separation }}
							</option>
						</select>

						<div v-if="weightSeparation">
							<!-- Set weights -->
							<div
								v-for="index of weightSeparations[weightSeparation].length"
								:key="index"
								class="inline-flex w-full">
								<span v-if="weightSeparations[weightSeparation].length === index">
									<PlusIcon class="h-5 w-5 relative top-1/2 -translate-y-1/2" />
								</span>
								<span v-else>
									<MinusIcon class="h-5 w-5 relative top-1/2 -translate-y-1/2" />
								</span>
								<input
									:id="`${weightSeparation}_${index}`"
									v-model="weightSeparations[weightSeparation][index - 1]"
									v-mask="'###'"
									type="text"
									class="appearance-none border-none bg-gray-100 rounded-lg m-1 text-center w-60" />
							</div>

							<!-- Add/remove weight category -->
							<div class="grid grid-cols-2 m-1 gap-x-2">
								<div
									class="text-green-800 bg-green-500 w-full rounded-lg px-1 py-2 cursor-pointer hover:bg-green-400"
									@click="weightSeparations[weightSeparation].push('')">
									<PlusIcon class="h-5 w-5 m-auto" />
								</div>
								<div
									class="text-red-800 bg-red-500 w-full rounded-lg px-1 py-2 cursor-pointer hover:bg-red-400"
									@click="weightSeparations[weightSeparation].pop()">
									<MinusIcon class="h-5 w-5 m-auto" />
								</div>
							</div>
						</div>
					</div>

					<!-- Continue button -->
					<Button
						class="mt-20"
						:loading="showSpinningWheel"
						:show-x="showX"
						:show-check="showCheck"
						:message="
							stateConfirm.separateBelt
								? t('setBeltsRange')
								: t('createTournamentsForThisCategory')
						"
						type="primary"
						@button-click="
							stateConfirm.separateBelt ? prepareBelts() : createTourns()
						" />
				</div>

				<!-- Set belts separations -->
				<div v-else-if="setBelts">
					<!-- Title and return button -->
					<div class="inline-flex w-full justify-between">
						<p class="text-xl text-left font-semibold">
							{{ categoryToConfirm.name }}
						</p>
						<Button
							class="max-w-max mb-2"
							:message="
								stateConfirm.separateWeight
									? t('returnToDefineWeights')
									: t('returnToDefineAges')
							"
							:icon-left="true"
							:icon="ArrowLeftIcon"
							:type="'black'"
							:size="'small'"
							@button-click="
								setBelts = false;
								stateConfirm.separateWeight
									? (setWeights = true)
									: (confirm = true);
							" />
					</div>

					<div class="w-full">
						<!-- Age/sex/weight separation selection -->
						<select
							id="beltSelect"
							v-model="beltSeparation"
							name="beltSelect"
							class="w-full text-center">
							<option
								v-for="separation in Object.keys(beltSeparations)"
								:key="separation"
								:value="separation">
								{{ separation }}
							</option>
						</select>

						<div v-if="beltSeparation">
							<!-- Set belts -->
							<div
								v-for="index of beltSeparations[beltSeparation].length"
								:key="index"
								class="inline-flex w-full gap-x-4">
								<SearchSelect
									class="w-full"
									:title="''"
									:name="`${beltSeparation}_min_${index}`"
									:option-selected="
										beltSeparations[beltSeparation][index - 1].min
									"
									:options="beltsList"
									:use-translations="true"
									:error="''"
									@selected="
										(option) =>
											(beltSeparations[beltSeparation][index - 1].min =
												option)
									" />
								<p class="my-auto text-xl font-bold">&mdash;</p>
								<SearchSelect
									class="w-full"
									:title="''"
									:name="`${beltSeparation}_max_${index}`"
									:option-selected="
										beltSeparations[beltSeparation][index - 1].max
									"
									:options="beltsList"
									:error="''"
									:use-translations="true"
									@selected="
										(option) =>
											(beltSeparations[beltSeparation][index - 1].max =
												option)
									" />
							</div>

							<!-- Add/remove belt category -->
							<div class="grid grid-cols-2 m-1 gap-x-2">
								<div
									class="text-green-800 bg-green-500 w-full rounded-lg px-1 py-2 cursor-pointer hover:bg-green-400"
									@click="
										beltSeparations[beltSeparation].push({
											min: '',
											max: '',
										})
									">
									<PlusIcon class="h-5 w-5 m-auto" />
								</div>
								<div
									class="text-red-800 bg-red-500 w-full rounded-lg px-1 py-2 cursor-pointer hover:bg-red-400"
									@click="beltSeparations[beltSeparation].pop()">
									<MinusIcon class="h-5 w-5 m-auto" />
								</div>
							</div>
						</div>
					</div>

					<!-- Continue button -->
					<Button
						class="mt-20"
						:loading="showSpinningWheel"
						:show-x="showX"
						:show-check="showCheck"
						:message="t('createTournamentsForThisCategory')"
						type="primary"
						@button-click="createTourns" />
				</div>

				<!-- Categories list -->
				<div v-else class="flex flex-col">
					<Button
						class="max-w-max ml-auto mb-2"
						:message="t('newCategory')"
						:icon-left="true"
						:size="'small'"
						:icon="PlusIcon"
						:type="'success'"
						@button-click="newCategory = true" />

					<!-- List of Categories -->
					<div
						v-for="category of categories"
						v-show="
							competitionCategories.findIndex((a) => a.name == category.name) === -1
						"
						:key="category.id"
						class="text-center group relative cursor-pointer text-lg my-1 rounded-md z-0 bg-gray-100">
						<p class="group-hover:opacity-25">
							{{ category.name }}
						</p>
						<div
							class="inset-y-0 left-0 right-1/4 absolute opacity-0 hover:opacity-75 z-10 bg-green-500 rounded-md"
							@click="
								categoryToConfirm = category;
								confirm = true;
							">
							<PlusIcon class="w-5 h-5 text-white mx-auto mt-1" />
						</div>
						<div
							class="inset-y-0 right-0 left-3/4 absolute opacity-0 hover:opacity-75 z-10 bg-amber-500 rounded-md"
							@click="fillEditCategory(category)">
							<PencilIcon class="w-5 h-5 text-white mx-auto mt-1" />
						</div>
					</div>

					<!-- List of Categories in the competition -->
					<p
						v-if="competitionCategories.length"
						class="mt-10 text-lg font-medium text-center">
						{{ t("editCategoriesOfTheCompetition") }}
					</p>
					<div
						v-for="category of competitionCategories"
						:key="category.id"
						class="text-center group relative cursor-pointer text-lg my-1 rounded-md z-0 bg-gray-100">
						<p class="group-hover:opacity-25">
							{{ category.name }}
						</p>
						<div
							class="inset-y-0 left-0 right-1/4 absolute opacity-0 hover:opacity-75 z-10 bg-green-500 rounded-md"
							@click="editCategoryTourn(category)">
							<PencilSquareIcon class="w-5 h-5 text-white mx-auto mt-1" />
						</div>
						<div
							class="inset-y-0 right-0 left-3/4 absolute opacity-0 hover:opacity-75 z-10 bg-amber-500 rounded-md"
							@click="fillEditCategory(category)">
							<PencilIcon class="w-5 h-5 text-white mx-auto mt-1" />
						</div>
					</div>
				</div>
			</div>
		</div>
	</Modal>
</template>

<script setup>
import Modal from "@/components/partials/modal.vue";
import Loading from "@/components/partials/loading.vue";
import Help from "@/components/partials/templates/help.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import ToogleInput from "@/components/partials/inputs/toogle.vue";
import Button from "@/components/partials/button.vue";
import {
	PlusIcon,
	ArrowLeftIcon,
	PencilIcon,
	MinusIcon,
	PencilSquareIcon,
} from "@heroicons/vue/24/solid";
import { useI18n } from "vue-i18n";
import { ref, watch, onMounted } from "vue";
import { authApi, errorHandling } from "@/services/api";
import toast from "@/toast.js";
import { required, helpers, maxLength } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";

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

const req = helpers.withMessage(t("error.required"), required);
const maxLen = helpers.withMessage(t("error.maxLen", { count: 255 }), maxLength(255));

const state = ref({
	name: "",
	thirdPlace: false,
	threePoints: false,
	rounds: false,
	penalties: false,
	numberAllAtOnce: false,
	type: "Tournament",
	teamCategory: false,
	teamNumber: 3,
});

const stateConfirm = ref({
	separateSex: false,
	separateAge: false,
	separateWeight: false,
	separateBelt: false,
});

const rules = {
	name: {
		required: req,
		max: maxLen,
	},
};

const v$ = useVuelidate(rules, state);
const showSpinningWheelImport = ref(false);
const categoriesTypes = ref([]);
const beltsList = ref([]);
const categoryTypeTounamentId = ref("");
const loading = ref(true);
const competitionCategories = ref([]);
const weightSeparation = ref("");
const confirm = ref(false);
const setWeights = ref(false);
const setBelts = ref(false);
const categoriesDefaults = ref([]);
const categories = ref([]);
const beltSeparation = ref("");
const newCategory = ref(false);
const editCategory = ref(false);
const categoryToEdit = ref(null);
const categoryToConfirm = ref(null);
const ageMasc = ref([]);
const ageFem = ref([]);
const weightSeparations = ref({});
const beltSeparations = ref({});
const categoryToUseDefault = ref(null);
const categoryImportError = ref(false);
const showSpinningWheel = ref(false);
const showCheck = ref(false);
const showX = ref(false);
const categoryPrice = ref(10);

watch(
	() => props.open,
	(after) => {
		if (after) {
			resetStateConfirm();
			getCategories();
		}
	}
);

onMounted(async () => {
	try {
		const [{ data: categoriesTypesData }, { data: beltsData }] = await Promise.all([
			authApi.get("categories-type"),
			authApi.get("belts"),
		]);
		categoriesTypes.value = categoriesTypesData;
		categoryTypeTounamentId.value = categoriesTypesData.find(
			(a) => a.name === "Tournament"
		)?.id;
		beltsList.value = beltsData.map((belt) => ({ ...belt, name: `belts.${belt.name}` }));
	} catch (e) {
		errorHandling(e);
	} finally {
		loading.value = false;
	}
});

const resetStateConfirm = () => {
	stateConfirm.value = {
		separateSex: false,
		separateAge: false,
		separateWeight: false,
		separateBelt: false,
	};
	ageMasc.value = [
		{ min: 5, max: 7 },
		{ min: 8, max: 10 },
		{ min: 11, max: 13 },
		{ min: 14, max: 15 },
		{ min: 16, max: 18 },
		{ min: 19, max: 39 },
		{ min: 40, max: 45 },
		{ min: 46, max: "" },
	];
	ageFem.value = [
		{ min: 5, max: 7 },
		{ min: 8, max: 10 },
		{ min: 11, max: 13 },
		{ min: 14, max: 15 },
		{ min: 16, max: 18 },
		{ min: 19, max: 35 },
		{ min: 36, max: 45 },
		{ min: 46, max: "" },
	];
	showCheck.value = false;
	showX.value = false;
	showSpinningWheel.value = false;
	showSpinningWheelImport.value = false;
	showX.value = false;
	confirm.value = false;
	setWeights.value = false;
	newCategory.value = false;
	editCategory.value = false;
	categoryPrice.value = 10;
	state.value = {
		name: "",
		thirdPlace: false,
		threePoints: false,
		rounds: false,
		penalties: false,
		numberAllAtOnce: false,
		teamCategory: false,
		teamNumber: 3,
		type: categoryTypeTounamentId.value,
	};
};

const getCategories = async () => {
	loading.value = true;
	try {
		const [
			{ data: competitionCategoriesData },
			{ data: categoriesDefaultData },
			{ data: allCategoriesData },
		] = await Promise.all([
			authApi.get(`categories?competition_id=${props.competitionId}&limit=-1`),
			authApi.get("categories?defaults=true&limit=-1"),
			authApi.get("categories?defaults=false&limit=-1"),
		]);
		categories.value = allCategoriesData.results;
		categoriesDefaults.value = categoriesDefaultData.results;
		competitionCategories.value = competitionCategoriesData.results;
	} catch (e) {
		errorHandling(e);
	} finally {
		loading.value = false;
	}
};

const fillEditCategory = (category) => {
	categoryToEdit.value = category;
	state.value.name = category.name;
	state.value.thirdPlace = category.third_place;
	state.value.threePoints = category.three_points;
	state.value.rounds = category.rounds;
	state.value.penalties = category.penalties;
	state.value.numberAllAtOnce = category.number_all_at_once;
	state.value.type = category.category_type.id;
	state.value.teamCategory = category.team_category;
	state.value.teamNumber = category.team_number;
	editCategory.value = true;
};

const closeCategory = () => {
	categoryToEdit.value = null;
	state.value.name = "";
	state.value.thirdPlace = false;
	state.value.threePoints = false;
	state.value.rounds = false;
	state.value.penalties = false;
	state.value.numberAllAtOnce = false;
	editCategory.value = false;
	newCategory.value = false;
};

const createOrUpdateCategory = async () => {
	showX.value = false;
	showCheck.value = false;
	showSpinningWheel.value = true;

	const requestData = {
		name: state.value.name,
		third_place: state.value.thirdPlace,
		three_points: state.value.threePoints,
		rounds: state.value.rounds,
		penalties: state.value.penalties,
		number_all_at_once: state.value.numberAllAtOnce,
		team_category: state.value.teamCategory,
		team_number: state.value.teamNumber,
		category_type_id: state.value.type,
	};

	try {
		await (newCategory.value
			? authApi.post("categories", requestData)
			: authApi.put(`categories/${categoryToEdit.value.id}`, requestData));
		showCheck.value = true;
		closeCategory();
		getCategories();
		resetStateConfirm();
	} catch (e) {
		showX.value = true;
		errorHandling(e);
	} finally {
		showSpinningWheel.value = false;
	}
};

const fillInputsEditCategory = (tournaments) => {
	if (!tournaments.length) return;
	const firstTournament = tournaments[0];
	stateConfirm.value.separateSex = firstTournament.is_male != null;
	stateConfirm.value.separateAge =
		firstTournament.age_min != null || firstTournament.age_max != null;
	stateConfirm.value.separateWeight =
		firstTournament.weight_min != null || firstTournament.weight_max != null;
	stateConfirm.value.separateBelt =
		firstTournament.belt_min_id != null || firstTournament.belt_max_id != null;

	ageMasc.value = [];
	ageFem.value = [];
	weightSeparations.value = {};
	beltSeparations.value = {};

	for (const tournament of tournaments) {
		if (tournament.age_min != null || tournament.age_max != null) {
			if (tournament.is_male == null || tournament.is_male) {
				if (
					ageMasc.value.findIndex(
						(a) => a.min == tournament.age_min && a.max == tournament.age_max
					) == -1
				) {
					ageMasc.value.push({ min: tournament.age_min, max: tournament.age_max });
				}
			} else {
				if (
					ageFem.value.findIndex(
						(a) => a.min == tournament.age_min && a.max == tournament.age_max
					) == -1
				) {
					ageFem.value.push({ min: tournament.age_min, max: tournament.age_max });
				}
			}
		}
		if (tournament.weight_min != null || tournament.weight_max != null) {
			const key =
				(tournament.is_male == null ? "" : tournament.is_male ? "Masc." : "Fem.") +
				(tournament.age_max == null && tournament.age_min == null
					? ""
					: (tournament.age_max == null ? "+" : "") +
					  (tournament.age_min == null ? "-" : tournament.age_min) +
					  (tournament.age_min == null || tournament.age_max == null ? "" : " - ") +
					  (tournament.age_max == null ? "" : tournament.age_max));
			if (key in weightSeparations.value) {
				weightSeparations.value[key].push(
					tournament.weight_min == null ? tournament.weight_max : tournament.weight_min
				);
				weightSeparations.value[key] = weightSeparations.value[key].sort();
			} else {
				weightSeparations.value[key] = [
					tournament.weight_min == null ? tournament.weight_max : tournament.weight_min,
				];
			}
		}
		if (tournament.belt_min_id != null && tournament.belt_max_id != null) {
			const key =
				(tournament.is_male == null ? "" : tournament.is_male ? "Masc." : "Fem.") +
				(tournament.age_max == null && tournament.age_min == null
					? ""
					: (tournament.age_max == null ? "+" : "") +
					  (tournament.age_min == null ? "-" : tournament.age_min) +
					  (tournament.age_min == null || tournament.age_max == null ? "" : " - ") +
					  (tournament.age_max == null ? "" : tournament.age_max)) +
				(tournament.weight_max == null && tournament.weight_min == null
					? ""
					: " " +
					  (tournament.weight_max == null ? "+" : "") +
					  (tournament.weight_min == null ? "-" : tournament.weight_min) +
					  (tournament.weight_min == null || tournament.weight_max == null
							? ""
							: " - ") +
					  (tournament.weight_max == null ? "" : tournament.weight_max) +
					  "Kg.");

			if (key in beltSeparations.value) {
				beltSeparations.value[key].push({
					min: tournament.belt_min_id,
					max: tournament.belt_max_id,
				});
				beltSeparations.value[key] = beltSeparations.value[key].sort((a, b) => {
					beltsList.value.find((c) => c.id == a)?.order -
						beltsList.value.find((c) => c.id == b)?.order;
				});
			} else {
				beltSeparations.value[key] = [
					{ min: tournament.belt_min_id, max: tournament.belt_max_id },
				];
			}
		}
	}
	ageMasc.value.sort((a, b) => {
		if (a.min == null) return -1;
		if (b.min == null) return 1;
		if (a.max == null) return 1;
		if (b.max == null) return -1;
		return a.min - b.min;
	});
	ageFem.value.sort((a, b) => {
		if (a.min == null) return -1;
		if (b.min == null) return 1;
		if (a.max == null) return 1;
		if (b.max == null) return -1;
		return a.min - b.min;
	});
};

const editCategoryTourn = async (category) => {
	categoryToConfirm.value = category;

	try {
		const { data } = await authApi.get(
			`tournaments?competition_id=${props.competitionId}&category_id=${category.id}&limit=-1&show_zero=true`
		);

		const tournaments = data.results;
		fillInputsEditCategory(tournaments);
		confirm.value = true;
	} catch (e) {
		errorHandling(e);
	}
};

const getSeparationsFromOtherCategory = async () => {
	categoryImportError.value = false;
	if (categoryToUseDefault.value == null || categoryToUseDefault.value == "") {
		categoryImportError.value = true;
		return;
	}

	showSpinningWheelImport.value = true;
	try {
		const { data } = await authApi.get(
			`tournaments?category_id=${categoryToUseDefault.value}&show_zero=true&limit=-1`
		);
		if (!data.results.length) return;
		fillInputsEditCategory(data.results);
	} catch (e) {
		errorHandling(e);
	} finally {
		showSpinningWheelImport.value = false;
	}
};

const confirmAge = (ageObj) => {
	let index = 0;
	let ageMaxAux = 0;
	for (let age of ageObj) {
		if (
			((age.min == "" || age.min == null) && index != 0) ||
			((age.max == "" || age.max == null) && index != ageObj.length - 1) ||
			isNaN(age.min) ||
			isNaN(age.max)
		) {
			toast.error(t("error.invalidAgeInTheLine", { line: index + 1 }));
			return false;
		}
		if (ageMaxAux == null) {
			toast.error(t("error.invalidAgeInTheLine", { line: index }));
			return false;
		}
		if (age.min == "" || age.min == null) {
			age.max = Number(age.max);
			age.min = null;
			ageMaxAux = age.max;
			index += 1;
			continue;
		}
		if ((age.max == "" || age.max == null) && age.min > ageMaxAux) {
			age.min = Number(age.min);
			age.max = null;
			ageMaxAux = age.max;
			index += 1;
			continue;
		}
		age.max = age.max == null ? null : Number(age.max);
		age.min = age.min == null ? null : Number(age.min);
		if (age.min >= age.max) {
			toast.error(t("error.leftAgeNotInferiorThanRightAge", { line: index + 1 }));
			return false;
		}
		if (age.min <= ageMaxAux) {
			toast.error(t("error.leftAgeNotSuperiorThanRightPreviousAge", { line: index + 1 }));
			return false;
		}
		ageMaxAux = age.max;
		index += 1;
	}
	return true;
};

const verifyAges = () => {
	if (stateConfirm.value.separateAge) {
		if (!confirmAge(ageMasc.value)) {
			return;
		}
		if (stateConfirm.value.separateSex) {
			if (!confirmAge(ageFem.value)) {
				return;
			}
		}
	}

	const weightAux = JSON.parse(JSON.stringify(weightSeparations.value));
	weightSeparations.value = {};
	if (stateConfirm.value.separateWeight) {
		if (stateConfirm.value.separateSex) {
			if (stateConfirm.value.separateAge) {
				for (const age of ageMasc.value) {
					const key =
						"Masc." +
						(age.max == null ? "+" : "") +
						(age.min == null ? "-" : age.min) +
						(age.min == null || age.max == null ? "" : " - ") +
						(age.max == null ? "" : age.max);
					if (key in weightAux) weightSeparations.value[key] = weightAux[key];
					else weightSeparations.value[key] = ["", "", "", "", "", "", ""];
				}
				for (let age of ageFem.value) {
					const key =
						"Fem." +
						(age.max == null ? "+" : "") +
						(age.min == null ? "-" : age.min) +
						(age.min == null || age.max == null ? "" : " - ") +
						(age.max == null ? "" : age.max);
					if (key in weightAux) weightSeparations.value[key] = weightAux[key];
					else weightSeparations.value[key] = ["", "", "", "", "", "", ""];
				}
			} else {
				if (!("Masc." in weightSeparations.value))
					weightSeparations.value["Masc."] = ["", "", "", "", "", "", ""];
				if (!("Fem." in weightSeparations.value))
					weightSeparations.value["Fem."] = ["", "", "", "", "", "", ""];
			}
		} else {
			if (stateConfirm.value.separateAge) {
				for (const age of ageMasc.value) {
					const key =
						(age.max == null ? "+" : "") +
						(age.min == null ? "-" : age.min) +
						(age.min == null || age.max == null ? "" : " - ") +
						(age.max == null ? "" : age.max);
					if (key in weightAux) weightSeparations.value[key] = weightAux[key];
					else weightSeparations.value[key] = ["", "", "", "", "", "", ""];
				}
			}
		}
	}

	weightSeparation.value = Object.keys(weightSeparations.value)[0];
	confirm.value = false;
	setWeights.value = true;
};

const prepareBelts = () => {
	if (stateConfirm.value.separateAge && !stateConfirm.value.separateWeight) {
		if (!confirmAge(ageMasc.value)) {
			return;
		}
		if (stateConfirm.value.separateSex) {
			if (!confirmAge(ageFem.value)) {
				return;
			}
		}
	}

	if (stateConfirm.value.separateWeight) {
		let errors = [];
		for (const index in weightSeparations.value) {
			let prevWeight = 0;
			if (weightSeparations.value[index].length == 0) {
				errors.push(t("error.weightsIndexInvalid", { index: index }));
			}
			for (const weightValue of weightSeparations.value[index]) {
				if (weightValue < prevWeight) {
					errors.push(t("error.weightsIndexInvalid", { index: index }));
					break;
				}
				prevWeight = weightValue;
			}
		}
		for (const error of errors) {
			toast.error(error);
		}
		if (errors.length != 0) {
			return;
		}
	}

	const beltAux = JSON.parse(JSON.stringify(beltSeparations.value));
	beltSeparations.value = {};

	if (stateConfirm.value.separateBelt) {
		if (stateConfirm.value.separateWeight) {
			for (const separationWeight in weightSeparations.value) {
				let length = weightSeparations.value[separationWeight].length - 1;
				let index = 0;
				for (let weight of weightSeparations.value[separationWeight]) {
					const key = separationWeight + (index == length ? " +" : " -") + weight + "Kg.";
					index += 1;
					if (key in beltAux) {
						beltSeparations.value[key] = beltAux[key];
						continue;
					}
					beltSeparations.value[key] = [
						{ min: "", max: "" },
						{ min: "", max: "" },
						{ min: "", max: "" },
					];
				}
			}
		} else {
			if (stateConfirm.value.separateSex) {
				if (stateConfirm.value.separateAge) {
					for (const age of ageMasc.value) {
						const key =
							"Masc." +
							(age.max == null ? "+" : "") +
							(age.min == null ? "-" : age.min) +
							(age.min == null || age.max == null ? "" : " - ") +
							(age.max == null ? "" : age.max);
						if (key in beltAux) beltSeparations.value[key] = beltAux[key];
						else
							beltSeparations.value[key] = [
								{ min: "", max: "" },
								{ min: "", max: "" },
								{ min: "", max: "" },
							];
					}
					for (const age of ageFem.value) {
						const key =
							"Fem." +
							(age.max == null ? "+" : "") +
							(age.min == null ? "-" : age.min) +
							(age.min == null || age.max == null ? "" : " - ") +
							(age.max == null ? "" : age.max);
						if (key in beltAux) beltSeparations.value[key] = beltAux[key];
						else
							beltSeparations.value[key] = [
								{ min: "", max: "" },
								{ min: "", max: "" },
								{ min: "", max: "" },
							];
					}
				} else {
					if (!("Masc." in beltSeparations.value))
						beltSeparations.value["Masc."] = [
							{ min: "", max: "" },
							{ min: "", max: "" },
							{ min: "", max: "" },
						];
					if (!("Fem." in beltSeparations.value))
						beltSeparations.value["Fem."] = [
							{ min: "", max: "" },
							{ min: "", max: "" },
							{ min: "", max: "" },
						];
				}
			} else {
				if (stateConfirm.value.separateAge) {
					for (let age of ageMasc.value) {
						let key =
							(age.max == null ? "+" : "") +
							(age.min == null ? "-" : age.min) +
							(age.min == null || age.max == null ? "" : " - ") +
							(age.max == null ? "" : age.max);
						if (key in beltAux) beltSeparations.value[key] = beltAux[key];
						else
							beltSeparations.value[key] = [
								{ min: "", max: "" },
								{ min: "", max: "" },
								{ min: "", max: "" },
							];
					}
				}
			}
		}
	}

	beltSeparation.value = Object.keys(beltSeparations.value)[0];
	confirm.value = false;
	setWeights.value = false;
	setBelts.value = true;
};

const createTourns = async () => {
	if (stateConfirm.value.separateBelt) {
		const errors = [];
		for (const index in beltSeparations.value) {
			let prevBelt = 0;
			if (beltSeparations.value[index].length == 0) {
				errors.push(t("error.beltsIndexInvalid", { index: index }));
			}
			for (const beltValue of beltSeparations.value[index]) {
				if (
					beltValue.min == "" ||
					beltValue.max == "" ||
					beltValue.min == null ||
					beltValue.max == null
				) {
					errors.push(t("error.beltsIndexInvalid", { index: index }));
					break;
				}
				let min = beltsList.value.find((a) => a.id == beltValue.min).order;
				let max = beltsList.value.find((a) => a.id == beltValue.max).order;
				if (min <= prevBelt || min > max) {
					errors.push(t("error.beltsIndexInvalid", { index: index }));
					break;
				}
				prevBelt = max;
			}
		}
		for (const error of errors) {
			toast.error(error);
		}
		if (errors.length != 0) {
			return;
		}
	} else {
		if (stateConfirm.value.separateWeight) {
			const errors = [];
			for (const index in weightSeparations.value) {
				let prevWeight = 0;
				if (weightSeparations.value[index].length == 0) {
					errors.push(t("error.weightsIndexInvalid", { index: index }));
				}
				const length = weightSeparations.value[index].length;
				let weightIndex = 0;
				for (const weightValue of weightSeparations.value[index]) {
					weightIndex += 1;
					if (weightValue <= prevWeight && weightIndex != length) {
						errors.push(t("error.weightsIndexInvalid", { index: index }));
						break;
					}
					prevWeight = weightValue;
				}
			}
			for (const error of errors) {
				toast.error(error);
			}
			if (errors.length != 0) {
				return;
			}
		}
	}

	showSpinningWheel.value = true;
	showX.value = false;
	showCheck.value = false;

	const tournaments = [];
	let tournamentAux = {
		category: categoryToConfirm.value.name,
		is_male: null,
		age_min: null,
		age_max: null,
		weight_min: null,
		weight_max: null,
		belt_min_id: null,
		belt_max_id: null,
		price: categoryPrice.value,
	};

	if (stateConfirm.value.separateBelt) {
		for (const beltIndex in beltSeparations.value) {
			tournamentAux.is_male = null;
			tournamentAux.age_min = null;
			tournamentAux.age_max = null;
			tournamentAux.weight_min = null;
			tournamentAux.weight_max = null;
			tournamentAux.belt_min_id = null;
			tournamentAux.belt_max_id = null;

			const matches = beltIndex.match(/[+-]{1}\d+Kg\./g);
			const separateByWeight = !(matches == null || matches.length == 0);

			if (beltIndex.indexOf("Masc.") != -1) tournamentAux.is_male = true;
			else if (beltIndex.indexOf("Fem.") != -1) tournamentAux.is_male = false;
			if (stateConfirm.value.separateAge) {
				let stringWithAge = separateByWeight ? beltIndex.split(matches[0])[0] : beltIndex;
				if (stateConfirm.value.separateSex)
					stringWithAge = stringWithAge.split(" ").slice(1).join(" ");
				if (stringWithAge.indexOf("+") != -1)
					tournamentAux.age_min = Number(stringWithAge.split("+")[1]);
				else if (stringWithAge.indexOf(" - ") != -1) {
					tournamentAux.age_min = Number(stringWithAge.split("-")[0]);
					tournamentAux.age_max = Number(stringWithAge.split("-")[1]);
				} else if (stringWithAge.indexOf("-") != -1)
					tournamentAux.age_max = Number(stringWithAge.split("-")[1]);
			}

			if (separateByWeight) {
				const match = matches[0].replace("Kg.", "");
				if (match.indexOf("-") != -1) {
					tournamentAux.weight_max = Number(match.replace("-", ""));
				} else if (match.indexOf("+") != -1) {
					tournamentAux.weight_min = Number(match.replace("+", ""));
				}
			}

			for (const beltsValue of beltSeparations.value[beltIndex]) {
				tournamentAux.belt_min_id = beltsValue.min;
				tournamentAux.belt_max_id = beltsValue.max;
				tournaments.push(JSON.parse(JSON.stringify(tournamentAux)));
			}
		}
	} else {
		if (stateConfirm.value.separateWeight) {
			for (const weightIndex in weightSeparations.value) {
				tournamentAux.is_male = null;
				tournamentAux.age_min = null;
				tournamentAux.age_max = null;
				tournamentAux.weight_min = null;
				tournamentAux.weight_max = null;
				console.log(weightIndex.indexOf("Masc."));
				if (weightIndex.indexOf("Masc.") != -1) tournamentAux.is_male = true;
				else if (weightIndex.indexOf("Fem.") != -1) tournamentAux.is_male = false;
				if (weightIndex.indexOf("+") != -1)
					tournamentAux.age_min = Number(weightIndex.split("+")[1]);
				else if (weightIndex.indexOf(" - ") != -1) {
					tournamentAux.age_min = Number(weightIndex.split("-")[0].split(" ")[1]);
					tournamentAux.age_max = Number(weightIndex.split("-")[1].split(" ")[1]);
				} else if (weightIndex.indexOf("-") != -1)
					tournamentAux.age_max = Number(weightIndex.split("-")[1]);

				let index = 1;
				for (let weights of weightSeparations.value[weightIndex]) {
					tournamentAux.weight_min = null;
					tournamentAux.weight_max = null;
					if (index == weightSeparations.value[weightIndex].length)
						tournamentAux.weight_min = Number(weights);
					else tournamentAux.weight_max = Number(weights);
					tournaments.push(JSON.parse(JSON.stringify(tournamentAux)));
					index += 1;
				}
			}
		} else {
			if (stateConfirm.value.separateAge) {
				for (const age of ageMasc.value) {
					tournamentAux.is_male = stateConfirm.value.separateSex ? true : null;
					tournamentAux.age_min = age.min;
					tournamentAux.age_max = age.max ? Number(age.max) : null;
					console.log(tournamentAux.age_min, tournamentAux.age_max);
					tournaments.push(JSON.parse(JSON.stringify(tournamentAux)));
				}
				if (stateConfirm.value.separateSex) {
					for (const age of ageFem.value) {
						tournamentAux.is_male = false;
						tournamentAux.age_min = age.min;
						tournamentAux.age_max = Number(age.max);
						tournaments.push(JSON.parse(JSON.stringify(tournamentAux)));
					}
				}
			} else if (stateConfirm.value.separateSex) {
				tournamentAux.is_male = true;
				tournaments.push(JSON.parse(JSON.stringify(tournamentAux)));
				tournamentAux.is_male = false;
				tournaments.push(JSON.parse(JSON.stringify(tournamentAux)));
			} else tournaments.push(tournamentAux);
		}
	}

	try {
		await authApi.post(`competitions/${props.competitionId}/tournaments/multi`, tournaments);
		getCategories();
		setTimeout(() => {
			setWeights.value = false;
			setBelts.value = false;
			categoryToConfirm.value = null;
			resetStateConfirm();
		}, 500);
		showCheck.value = true;
	} catch (e) {
		errorHandling(e);
		showX.value = true;
	} finally {
		showSpinningWheel.value = false;
	}
};
</script>
