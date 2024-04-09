<template>
	<InsuranceGroupModal
		:open="openModal"
		@updated="getInsuranceGroups"
		@close="openModal = false" />
	<Modal :open="props.open" :outside-click="true" :show-x="true" @close="emit('close')">
		<Loading v-if="loading" :size="10" />
		<div v-else class="-mt-8">
			<p class="text-2xl font-medium">
				{{ t("addInsurancesToAGroup", { count: props.ids.length }) }}
			</p>
			<SearchSelect
				:title="t('forms.insuranceGroup')"
				:option-selected="insuranceGroup"
				:options="insuranceGroups"
				:error="''"
				@selected="
					(option) => {
						insuranceGroup = option;
					}
				" />
			<div class="w-full mt-4 inline-flex">
				<div class="w-full" />
				<Button
					class="max-w-max min-w-max"
					:message="t('createNewInsuranceGroup')"
					:type="'success'"
					:pill="true"
					:icon-left="true"
					:icon="PlusIcon"
					@button-click="openModal = true" />
				<div class="w-full" />
			</div>
			<div class="space-x-16 mt-4 mx-auto max-w-max">
				<Button
					class="max-w-max px-8"
					:message="t('cancel')"
					:type="'primary'"
					:pill="true"
					@button-click="emit('close')" />
				<Button
					class="max-w-max px-8"
					:message="t('add')"
					:type="'success'"
					:pill="true"
					@button-click="addInsurancesToGroup" />
			</div>
		</div>
	</Modal>
</template>

<script setup>
import Modal from "@/components/partials/modal.vue";
import Loading from "@/components/partials/loading.vue";
import InsuranceGroupModal from "@/components/admin/modals/insuranceGroup.vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import { PlusIcon } from "@heroicons/vue/24/solid";
import Button from "@/components/partials/button.vue";
import { ref, onMounted } from "vue";
import { authApi, errorHandling } from "@/services/api";
import { useI18n } from "vue-i18n";

let { t } = useI18n({ useScope: "global" });
const emit = defineEmits(["close", "added"]);

const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	insurancesIds: {
		type: String,
		required: false,
		defalt: "",
	},
	ids: {
		type: Array,
		reuqired: true,
	},
});

const insuranceGroups = ref([{ id: null, name: "none" }]);
const insuranceGroup = ref(null);
const openModal = ref(false);
const loading = ref(true);

const getInsuranceGroups = async () => {
	loading.value = true;
	try {
		const { data } = await authApi.get("insurance-groups");
		insuranceGroups.value.push(...data);
	} catch (e) {
		errorHandling(e);
	} finally {
		loading.value = false;
	}
};

onMounted(async () => {
	getInsuranceGroups();
});

const addInsurancesToGroup = async () => {
	loading.value = true;
	try {
		const { data } = await authApi.put(`insurances/multi/insurance-groups`, {
			ids: props.ids,
			insurance_group_id: insuranceGroup.value,
		});
		emit("added");
		emit("close");
	} catch (e) {
		errorHandling(e);
	} finally {
		loading.value = false;
	}
};
</script>
