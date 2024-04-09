<template>
	<div>
		<AddCategoryModal
			:open="openModal"
			:competition-id="props.competitionId"
			@close="
				openModal = false;
				reloadCompetition();
			" />
		<Loading v-if="loading" :size="10" />
		<div v-else class="p-6 text-center text-black">
			<div class="inline-flex justify-between w-full">
				<p class="text-3xl font-bold text-left mb-8">
					{{ t("titleDetails", { name: competition.name }) }}
				</p>
			</div>

			<div class="grid grid-cols-12 gap-y-6">
				<div class="col-span-12 lg:col-span-6">
					<div class="space-y-4">
						<div class="max-w-max">
							<div class="inline-flex rounded-md shadow-sm">
								<button
									type="button"
									:class="[
										'relative inline-flex items-center px-4 py-2 rounded-l-md border text-sm font-medium text-gray-700 hover:bg-gray-50 focus:z-10 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500',
										calculateAgeStartYear
											? 'bg-blue-200 border-blue-500 border-r-2'
											: 'bg-white border-gray-300',
									]"
									@click="
										() => {
											if (!calculateAgeStartYear) {
												calculateAgeStartYear = true;
												updateYearCalculation();
											}
										}
									">
									{{ t("ageStartYear") }}
								</button>
								<button
									type="button"
									:class="[
										'-ml-px relative inline-flex items-center px-4 py-2 rounded-r-md border text-sm font-medium text-gray-700 hover:bg-gray-50 focus:z-10 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500',
										!calculateAgeStartYear
											? 'bg-blue-200 border-blue-500'
											: 'border-l-0 bg-white border-gray-300 ',
									]"
									@click="
										() => {
											if (calculateAgeStartYear) {
												calculateAgeStartYear = false;
												updateYearCalculation();
											}
										}
									">
									{{ t("ageFirstDay") }}
								</button>
							</div>
						</div>
						<div class="min-w-max">
							<ToogleInput
								:label="t('public')"
								:sub-label="''"
								:option-selected="makePublic"
								@value-changed="
									(option) => {
										makePublic = option;
										updateVisibility();
									}
								" />
						</div>
						<div class="max-w-min">
							<Button
								:message="t('inscriptions')"
								type="primary"
								size="small"
								@button-click="
									router.push({
										name: 'Competition Inscriptions',
										params: { competitionId: competition.id },
									})
								" />
						</div>
					</div>
				</div>
				<div class="col-span-12 lg:col-span-6">
					<div>
						<TextArea
							name="notes"
							:label="t('notes')"
							:option-selected="notes"
							:error="''"
							@value-changed="(option) => (notes = option)" />
					</div>
					<div class="max-w-min min-w-max mt-2 ml-auto">
						<Button
							:message="t('updateNotes')"
							type="primary"
							size="small"
							@button-click="updateNotes" />
					</div>
				</div>
				<div class="col-span-6 col-start-1 text-xl font-medium text-center flex flex-col">
					<p>{{ t("dates") }}</p>
					<div class="relative mt-6 -mb-4 w-40 ml-auto">
						<Button
							:message="t('edit.dates')"
							type="primary"
							size="small"
							@button-click="
								router.push({
									name: 'Competition Edit Dates',
									params: { competitionId: competition.id },
								})
							" />
					</div>
				</div>
				<div class="col-span-6 col-start-7 text-xl font-medium text-center flex flex-col">
					<p>{{ t("categories") }}</p>
					<div class="relative mt-6 -mb-4 w-40 ml-auto">
						<Button
							:message="t('edit.categories')"
							type="primary"
							size="small"
							@button-click="openModal = true" />
					</div>
				</div>
				<div class="col-start-1 relative col-span-3">
					<Calendar :events="[]" :start="startArray" :end="endArray" />
				</div>

				<div class="col-start-4 col-span-3 space-y-4 mt-20 flex flex-col ml-14">
					<p class="text-lg font-medium">{{ t("legend") }}</p>
					<div class="inline-flex max-w-max mx-auto">
						<div class="w-7 h-7 bg-green-200 border border-black rounded-full" />
						<p class="ml-2">{{ t("days.inscriptions") }}</p>
					</div>
					<div class="inline-flex max-w-max mx-auto">
						<div class="w-7 h-7 bg-amber-200 border border-black rounded-full" />
						<p class="ml-2">{{ t("days.competition") }}</p>
					</div>
					<div class="inline-flex max-w-max mx-auto">
						<div class="w-7 h-7 bg-blue-200 border border-black rounded-full" />
						<p class="ml-2">{{ t("days.today") }}</p>
					</div>
				</div>

				<div class="col-start-7 col-span-6">
					<div class="flex flex-col text-lg font-medium max-w-max mx-auto">
						<div
							v-for="(category, index) of categories"
							:key="category.id"
							:class="[
								'px-4 py-1 rounded-lg',
								index % 2 == 0 ? 'bg-blue-100' : 'bg-white',
							]">
							{{ category.name }}
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import ToogleInput from "@/components/partials/inputs/toogle.vue";
import TextArea from "@/components/partials/inputs/textAreaInput.vue";
import Loading from "@/components/partials/loading.vue";
import AddCategoryModal from "@/components/competition/modals/addCategory.vue";
import Calendar from "@/components/partials/inputs/calendar.vue";
import Button from "@/components/partials/button.vue";
import { ref } from "vue";
import { authApi, errorHandling } from "@/services/api";
import router from "@/router";
import { useI18n } from "vue-i18n";

let { t } = useI18n();
let competition = ref(null);
let categories = ref([]);
let startArray = ref([]);
let endArray = ref([]);
let openModal = ref(false);
let loading = ref(true);
let makePublic = ref(false);
let calculateAgeStartYear = ref(false);
let notes = ref("");

const props = defineProps({
	// Competition ID
	competitionId: {
		type: String,
		required: true,
	},
});

const reloadCompetition = async () => {
	loading.value = true;
	try {
		const [{ data }, { data: categoriesPage }] = await Promise.all([
			authApi.get(`competitions/no-list/${props.competitionId}`),
			authApi.get(`categories?competition_id=${props.competitionId}&limit=-1`),
		]);

		categories.value = categoriesPage.results;
		getCompetition(data);
	} catch (e) {
		errorHandling(e);
	} finally {
		loading.value = false;
	}
};
reloadCompetition();

function getCompetition(data) {
	startArray.value = [
		{ date: new Date(data.inscriptions_start), color: "green" },
		{ date: new Date(data.competition_start), color: "amber" },
	];
	endArray.value = [
		{ date: new Date(data.inscriptions_end), color: "green" },
		{ date: new Date(data.competition_end), color: "amber" },
	];
	makePublic.value = data.show_public;
	calculateAgeStartYear.value = data.calculate_age_start_year || false;
	notes.value = data.notes;
	competition.value = data;
}

function updateVisibility() {
	loading.value = true;
	authApi
		.put(`competitions/make-public/${props.competitionId}`, { show_public: makePublic.value })
		.then((response) => {
			getCompetition(response.data);
			loading.value = false;
		})
		.catch((error) => {
			errorHandling(error, true);
			loading.value = false;
		});
}

function updateNotes() {
	loading.value = true;
	console.log(notes.value);
	authApi
		.put(`competitions/${props.competitionId}/notes`, { notes: notes.value })
		.then((response) => {
			getCompetition(response.data);
			loading.value = false;
		})
		.catch((error) => {
			errorHandling(error, true);
			loading.value = false;
		});
}

function updateYearCalculation() {
	loading.value = true;
	authApi
		.put(`competitions/year-calculation/${props.competitionId}`, {
			calculate_age_start_year: calculateAgeStartYear.value,
		})
		.then((response) => {
			getCompetition(response.data);
			loading.value = false;
		})
		.catch((error) => {
			errorHandling(error, true);
			loading.value = false;
		});
}
</script>

<i18n>
{
  	"en_GB": {
		"inscriptions": "Inscriptions",
		"public": "Show to Public",
		"titleDetails": "Competition {name} Details",
		"legend": "Legend: ",
		"days": {
			"inscriptions": "-- Inscriptions Days",
			"competition": "-- Competition Days",
			"today": "-- Today"
		},
		"dates": "Competition Dates",
		"categories": "Categories",
		"athletesLate": "Athletes with late inscriptions",
		"edit": {
			"dates": "Edit Dates",
			"categories": "Edit Categories",
			"inscriptions": "Edit Inscriptions"
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
			"duan-3": "Duan 3+"
		},
		"masc": "Masc.",
		"fem": "Fem.",
		"ageFirstDay": "Calculate athlete age in the first day of the competiton",
		"ageStartYear": "Calculate athlete age in the start of the year",
		"notes": "Admin Notes",
		"updateNotes": "Update Notes",
	},
	"pt_PT": {
		"inscriptions": "Inscrições",
		"public": "Mostrar ao Público",
		"title": "Detalhes da Competição {name}",
		"legend": "Legenda: ",
		"days": {
			"inscriptions": "-- Dias de inscrições",
			"competition": "-- Dias da competição",
			"today": "-- Hoje"
		},
		"dates": "Datas da Competição",
		"categories": "Categorias",
		"athletesLate": "Atletas com inscrições em atraso",
		"edit": {
			"dates": "Editar Datas",
			"categories": "Editar Categorias",
			"inscriptions": "Editar Inscrições"
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
			"duan-3": "Duan 3+"
		},
		"masc": "Masc.",
		"fem": "Fem.",
		"ageFirstDay": "Calcular idade do atleta no primeiro dia da competição",
		"ageStartYear": "Calcular idade do atleta no ínicio do ano"
	}
}
</i18n>
