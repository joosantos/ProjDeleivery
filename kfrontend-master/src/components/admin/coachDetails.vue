<template>
	<InsuranceCoachModal
		:open="openModal"
		:coach="coach"
		:insurance-id="modalInsuranceId"
		@updated="getCoach"
		@close="
			openModal = false;
			modalInsuranceId = '';
		" />
	<h1 class="text-left text-3xl font-semibold">{{ t("coach") }}</h1>
	<Loading v-if="loading" :size="10" />
	<div v-else class="mt-2">
		<p class="text-medium text-xl">
			{{ coach.name }}
		</p>
		<div id="insuranceInformationForm" class="scroll-mt-44 mt-4">
			<div class="shadow sm:overflow-hidden sm:rounded-md">
				<div class="lg:w-1/2 mx-8 mt-4">
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
				<div class="space-y-6 bg-white py-6 px-4 sm:p-6">
					<div>
						<h3 class="text-lg font-medium leading-6 text-gray-900">
							{{ t("insurance.title") }}
						</h3>
						<p class="mt-1 text-sm text-gray-500">
							{{ t("insurance.sub") }}
						</p>
					</div>
					<div class="grid grid-cols-12 gap-6">
						<p
							v-if="
								coach.insured_entity == null ||
								coach.insured_entity.insurances.length == 0
							"
							class="cols-pan-12 sm:col-span-9 text-xl font-medium text-center">
							{{ t("insurance.none") }}
						</p>
						<div v-else class="col-span-12 sm:col-span-12 space-y-4">
							<div
								v-for="insurance of coach.insured_entity.insurances"
								:key="insurance.id">
								<div
									class="w-full grid grid-cols-12 bg-blue-100 rounded-full px-8 py-2">
									<p
										class="col-span-12 text-center sm:text-left sm:col-span-6 lg:col-span-4">
										{{
											insurance.insurance_group != null
												? t("insurance.group", {
														group: insurance.insurance_group.name,
												  })
												: t("insurance.noGroup")
										}}
									</p>
									<p
										class="col-span-12 text-center sm:text-left sm:col-span-6 lg:col-span-4">
										{{
											t("insurance.type", {
												type: insurance.insurance_type.name,
											})
										}}
									</p>
									<p class="col-span-full text-center sm:text-left lg:col-span-4">
										{{
											t("insurance.date", {
												dateStart: translateDateFromApi(
													insurance.insurance_start_date
												),
												dateEnd: translateDateFromApi(
													insurance.insurance_end_date
												),
											})
										}}
									</p>
									<div
										class="col-span-full inline-flex justify-center space-x-8 mt-2">
										<button
											type="button"
											class="inline-flex justify-center rounded-md border border-transparent bg-yellow-500 py-1 px-4 text-sm font-medium text-white shadow-sm hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:ring-offset-2"
											@click.prevent="
												modalInsuranceId = insurance.id;
												openModal = true;
											">
											{{ t("insurance.edit") }}
										</button>
										<button
											type="button"
											class="inline-flex justify-center rounded-md border border-transparent bg-red-600 py-1 px-4 text-sm font-medium text-white shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
											@click.prevent="deleteInsurance(insurance.id)">
											{{ t("insurance.delete") }}
										</button>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div class="grid grid-cols-12 bg-gray-50 px-4 py-3 text-right sm:px-6">
					<div class="col-span-12 sm:col-span-7 sm:col-start-2">
						<Button
							:message="t('insurance.create')"
							:type="'primary'"
							:pill="true"
							@button-click="openModal = true" />
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import Loading from "@/components/partials/loading.vue";
import InsuranceCoachModal from "@/components/admin/modals/insuranceCoach.vue";
import TextArea from "@/components/partials/inputs/textAreaInput.vue";
import Button from "@/components/partials/button.vue";
import { ref } from "vue";
import { authApi, errorHandling, translateDateFromApi } from "@/services/api";
import { useI18n } from "vue-i18n";

const props = defineProps({
	coachId: {
		type: String,
		required: true,
	},
});

let { t } = useI18n();
let loading = ref(true);
let coach = ref([]);
let openModal = ref(false);
let modalInsuranceId = ref("");
let notes = ref("");

function getCoach() {
	authApi
		.get(`users/${props.coachId}`)
		.then((response) => {
			coach.value = response.data;
			notes.value = response.data.notes;
			loading.value = false;
		})
		.catch((error) => {
			errorHandling(error);
			loading.value = false;
		});
}
getCoach();

function updateNotes() {
	loading.value = true;
	authApi
		.put(`users/${props.coachId}`, { notes: notes.value })
		.then((response) => {
			coach.value = response.data;
			notes.value = response.data.notes;
			loading.value = false;
		})
		.catch((error) => {
			errorHandling(error);
			loading.value = false;
		});
}
</script>

<i18n>
{
	"en_GB": {
		"insurance": {
			"title": "Coach's Insurance Information",
			"sub": "This information is only available for the admins",
			"none": "This Coach has no insurances yet",
			"create": "Create a new Insurance",
			"edit": "Edit",
			"delete": "Delete",
			"noGroup": "No Insurance Group",
			"group": "Group: {group}",
			"type": "Type: {type}",
			"date": "From {dateStart} to {dateEnd}",
		},
		"notes": "Notes",
		"updateNotes": "Update Notes",
        "coach": "Coach Details",
	},
	"pt_PT": {
	}
}
</i18n>
