<template>
	<Loading v-if="loading" :size="10" />
	<div v-else class="grid mx-auto">
		<FederationRequestDenyModal
			:open="open"
			:federationRequestID="idOfRequestToDeny"
			:reason="reasonToModal"
			@close="open = false"
			@submit="
				(federationRequestID, reason) => patchRequest(federationRequestID, 'denied', reason)
			" />
		<div class="mt-4 inline-flex gap-x-8 mx-auto max-w-max">
			<CustomInput
				:label="t('season')"
				type="text"
				:name="'season'"
				:mask="'####'"
				:option-selected="form.season"
				:error="''"
				@value-changed="(option) => (form.season = option)" />
			<CustomInput
				v-if="isAdmin"
				:label="t('team')"
				type="text"
				:name="'team'"
				:option-selected="form.team"
				:error="''"
				@value-changed="(option) => (form.team = option)" />
			<CustomInput
				:label="t('athlete.name')"
				type="text"
				:name="'name'"
				:option-selected="form.name"
				:error="''"
				@value-changed="(option) => (form.name = option)" />
			<SearchSelect
				:options="STATUS"
				:title="t('status')"
				:option-selected="form.status"
				:error="''"
				:useTranslations="true"
				@selected="(option) => (form.status = option)"
				@loading="loadingAthletes" />
			<div class="min-w-max mt-auto">
				<Button
					:message="t('federationRequest.see')"
					type="primary"
					size="small"
					:loading="loadingAthletes"
					@button-click="getFederationRequests" />
			</div>
		</div>
		<div v-if="totalPages != 0" class="mx-auto mt-4 max-w-max">
			<div class="max-w-max mx-auto">
				<Pagination :pages="totalPages" :current="currentPage" @page-change="changePage" />
			</div>
			<div>
				<div
					v-for="federationRequest of federationRequests"
					v-show="federationRequest.athlete != null"
					:key="federationRequest.id"
					class="mt-4 px-2 rounded w-[32rem]">
					<div class="inline-flex w-full justify-between">
						<p class="text-xl font-medium">
							{{
								`${federationRequest?.athlete?.name} (${federationRequest?.athlete.team?.abbreviation})`
							}}
						</p>
						<i18n-t
							:keypath="
								federationRequest.id == null
									? 'federationRequest.neverRequested'
									: `federationRequest.${federationRequest.status || 'other'}`
							"
							tag="label"
							for="federationRequest.status"
							:class="[
								'capitalize font-medium min-w-max',
								federationRequest.status == 'pending' ||
								federationRequest.status == 'requested' ||
								federationRequest.id == null
									? 'text-blue-500'
									: federationRequest.status == 'accepted'
									? 'text-green-500'
									: federationRequest.status == 'denied'
									? 'text-red-500'
									: federationRequest.status == 'cancelled'
									? 'text-orange-500'
									: 'text-black',
							]">
							<span class="text-black">{{ $t("federationRequest.status") }}</span>
						</i18n-t>
					</div>
					<div class="w-full">
						<Loading v-if="federationRequest.loading" :size="1.5" />
						<div v-else-if="isAdmin" class="inline-flex justify-between w-full">
							<div class="max-w-max">
								<Button
									:message="t('federationRequest.deny')"
									type="danger"
									size="small"
									:disabled="federationRequest.status == 'denied'"
									:loading="federationRequest.loading"
									@button-click="
										openModal(federationRequest.id, federationRequest.notes)
									" />
							</div>
							<div class="max-w-max">
								<Button
									v-if="federationRequest.id == null"
									:message="t('federationRequest.create')"
									type="success"
									size="small"
									:disabled="federationRequest.status == 'accepted'"
									:loading="federationRequest.loading"
									@button-click="
										patchRequest(federationRequest.id, 'accepted')
									" />
								<Button
									v-else
									:message="t('federationRequest.accept')"
									type="primary"
									size="small"
									:disabled="federationRequest.status == 'accepted'"
									:loading="federationRequest.loading"
									@button-click="
										patchRequest(federationRequest.id, 'accepted')
									" />
							</div>
						</div>
						<div v-else class="inline-flex justify-between w-full">
							<div class="max-w-max">
								<Button
									v-if="
										federationRequest.status == 'denied' &&
										federationRequest.notes != ''
									"
									:message="t('federationRequest.seeDenyReason')"
									type="primary"
									size="small"
									@button-click="openModal('', federationRequest.notes)" />
							</div>
							<div class="max-w-max">
								<Button
									:message="
										t(
											federationRequest.id == null
												? 'federationRequest.request'
												: coachCanRequested(federationRequest.status)
												? 'federationRequest.rerequest'
												: federationRequest.status == 'accepted'
												? 'federationRequest.federated'
												: 'federationRequest.request'
										)
									"
									:type="
										coachCanRequested(federationRequest.status)
											? 'warning'
											: federationRequest.status == 'accepted'
											? 'success'
											: 'primary'
									"
									size="small"
									:disabled="
										federationRequest.id != null &&
										!coachCanAct(federationRequest.status)
									"
									:loading="federationRequest.loading"
									@button-click="patchRequest(federationRequest.id, 'pending')" />
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<NoResults v-else class="mx-auto mt-4" />
	</div>
</template>

<script setup>
import Loading from "@/components/partials/loading.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import { ref } from "vue";
import Button from "@/components/partials/button.vue";
import { authApi, errorHandling } from "@/services/api";
import { useI18n } from "vue-i18n";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import Pagination from "@/components/partials/pagination/pagination.vue";
import NoResults from "@/components/partials/pagination/noResults.vue";
import FederationRequestDenyModal from "@/components/admin/modals/federationRequestDenyModal.vue";
import store from "@/store";

let { t } = useI18n({ useScope: "global" });
let loading = ref(true);
let loadingAthletes = ref(false);
let federationRequests = ref([]);
let currentPage = ref(1);
let totalPages = ref(0);
let open = ref(false);
let idOfRequestToDeny = ref("");
let isAdmin = ref(store.getters.getUserRole == "ADMIN");
let reasonToModal = ref("");

const props = defineProps({
	teamId: {
		type: String,
		required: false,
		default: "",
	},
});

const FORM_DEFAULT = {
	season: `${new Date(Date.now()).getFullYear()}`,
	team: "",
	name: "",
	status: isAdmin.value ? "pending" : "accepted",
};
const STATUS = [
	{ name: "all", id: "all" },
	{ name: "withoutFederationRequest", id: "without" },
	{ name: "pending", id: "pending" },
	{ name: "accepted", id: "accepted" },
	{ name: "cancelled", id: "cancelled" },
	{ name: "denied", id: "denied" },
];

let form = ref(FORM_DEFAULT);

function getFederationRequests() {
	loadingAthletes.value = true;
	let url = `federation-requests?year=${form.value.season}&team=${
		props.teamId || form.value.team
	}&name=${form.value.name}&skip=${(currentPage.value - 1) * 20}&limit=20`;

	if (form.value.status == "all" || form.value.status == "without") {
		url += "&show_without=true";
	} else {
		url += `&status=${form.value.status}&show_without=false`;
	}

	authApi
		.get(url)
		.then((response) => {
			federationRequests.value = response.data.elements;
			totalPages.value = Math.ceil(response.data.total_elements_count / 20);
		})
		.catch((error) => {
			errorHandling(error);
		})
		.finally(() => {
			loading.value = false;
			loadingAthletes.value = false;
		});
}
getFederationRequests();

function changePage(pageNumber) {
	currentPage.value = pageNumber;
	getFederationRequests();
}

function openModal(federationRequestID, reason) {
	open.value = true;
	idOfRequestToDeny.value = federationRequestID;
	reasonToModal.value = reason;
}

function patchRequest(requestID, status, denyReason = "") {
	let index = federationRequests.value.findIndex((a) => a.id == requestID);
	if (index != -1) federationRequests.value[index].loading = true;

	if (requestID == null) {
		authApi
			.post(`federation-requests`, {
				athlete_id: federationRequests.value[index].athlete_id,
				year: form.value.season,
			})
			.then((response) => {
				if (index != -1) {
					federationRequests.value[index] = response.data;
					federationRequests.value[index].loading = false;
				}
			})
			.catch((error) => {
				errorHandling(error);
				if (index != -1) federationRequests.value[index].loading = false;
			});
		return;
	}

	authApi
		.patch(`federation-requests/${requestID}`, { status: status, notes: denyReason })
		.then((response) => {
			if (index != -1) {
				federationRequests.value[index] = response.data;
				federationRequests.value[index].loading = false;
			}
		})
		.catch((error) => {
			errorHandling(error);
			if (index != -1) federationRequests.value[index].loading = false;
		});
}

function coachCanRequested(federationRequestStatus) {
	return ["cancelled", "denied", "other"].findIndex((a) => a == federationRequestStatus) != -1;
}

function coachCanAct(federationRequestStatus) {
	return federationRequestStatus == "" || coachCanRequested(federationRequestStatus);
}
</script>
