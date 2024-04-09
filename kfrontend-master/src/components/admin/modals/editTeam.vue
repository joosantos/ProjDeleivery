<template>
	<Modal :open="props.open" :outside-click="true" :show-x="true" @close="emit('close')">
		<Loading v-if="loading" :size="10" />
		<div v-else>
			<p class="text-xl font-semibold text-center mb-4">
				{{ t("edit") }}
			</p>
			<div class="w-full space-y-4">
				<CustomInput
					:label="t('name')"
					type="text"
					:name="'name'"
					:option-selected="state.name"
					:error="!v$.name.$errors.length ? '' : v$.name.$errors[0].$message"
					@value-changed="(option) => (state.name = option)" />
				<CustomInput
					:label="t('abbreviation')"
					type="text"
					:name="'abbreviation'"
					:option-selected="state.abbreviation"
					:error="
						!v$.abbreviation.$errors.length ? '' : v$.abbreviation.$errors[0].$message
					"
					@value-changed="(option) => (state.abbreviation = option)" />
				<CustomInput
					:label="t('association')"
					type="text"
					:name="'association'"
					:option-selected="state.association"
					:error="
						!v$.association.$errors.length ? '' : v$.association.$errors[0].$message
					"
					@value-changed="(option) => (state.association = option)" />
				<CustomInput
					v-if="store.getters.getUserRole === 'ADMIN'"
					:label="t('forms.federationNumber')"
					type="text"
					:v-mask="'#####'"
					:name="'federationNumber'"
					:option-selected="state.federationNumber"
					:error="''"
					@value-changed="(option) => (state.federationNumber = option)" />

				<SearchSelect
					class="w-full"
					:options="REGIONS"
					:title="t('forms.region')"
					:option-selected="state.region"
					:use-translations="true"
					:error="''"
					@selected="(option) => (state.region = option)" />

				<SearchSelect
					class="w-full"
					:options="DISTRICTS"
					:title="t('forms.district')"
					:option-selected="state.district"
					:use-translations="true"
					:error="''"
					@selected="(option) => (state.district = option)" />
			</div>
			<div class="relative w-60 left-1/2 -translate-x-1/2 mt-60">
				<Button
					:loading="showSpinningWheel"
					:show-x="showX"
					:show-check="showCheck"
					:message="t('update')"
					type="primary"
					@button-click="updateTeam" />
			</div>
		</div>
	</Modal>
</template>

<script setup>
import Modal from "@/components/partials/modal.vue";
import Loading from "@/components/partials/loading.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import Button from "@/components/partials/button.vue";
import { useI18n } from "vue-i18n";
import { ref, watch } from "vue";
import { authApi, errorHandling } from "@/services/api";
import { required, helpers, maxLength } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import REGIONS from "@/constants/regions";
import DISTRICTS from "@/constants/districts";
import store from "@/store";
import toast from "@/toast.js";

const { t } = useI18n({ useScope: "global" });
const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	teamId: {
		type: String,
		required: true,
	},
});
const emit = defineEmits(["close"]);

const loading = ref(true);
const showSpinningWheel = ref(false);
const showCheck = ref(false);
const showX = ref(false);

const req = helpers.withMessage(t("error.required"), required);
const maxLen = helpers.withMessage(t("error.maxLen", { count: 255 }), maxLength(255));
const maxLenAbr = helpers.withMessage(t("error.maxLen", { count: 8 }), maxLength(8));

const state = ref({
	name: "",
	abbreviation: "",
	association: "",
	federationNumber: "",
	region: "",
	district: "",
});

const rules = {
	name: {
		required: req,
		max: maxLen,
	},
	abbreviation: {
		required: req,
		max: maxLenAbr,
	},
	association: {
		required: req,
		max: maxLen,
	},
	region: {
		required: req,
	},
	district: {
		required: req,
	},
};
const v$ = useVuelidate(rules, state);

watch(
	() => props.open,
	(after) => {
		if (!after) return;

		showSpinningWheel.value = false;
		showCheck.value = false;
		showX.value = false;
		v$.value.$reset();

		if (props.teamId != "") getTeam();
	}
);

const getTeam = async () => {
	loading.value = true;
	try {
		const { data } = await authApi.get(`teams/${props.teamId}`);
		state.value.name = data.name;
		state.value.abbreviation = data.abbreviation;
		state.value.association = data.association;
		state.value.federationNumber = data.federation_number;
		state.value.region = data.region;
		state.value.district = data.district;
	} catch (e) {
		errorHandling(e);
	} finally {
		loading.value = false;
	}
};

const updateTeam = async () => {
	showX.value = false;
	showCheck.value = false;
	showSpinningWheel.value = true;

	const isFormValid = await v$.value.$validate();
	if (!isFormValid) {
		showX.value = true;
		showSpinningWheel.value = false;
		return;
	}
	try {
		await authApi.put(`teams/${props.teamId}`, {
			name: state.value.name,
			abbreviation: state.value.abbreviation,
			association: state.value.association,
			federation_number: state.value.federationNumber || null,
			region: state.value.region,
			district: state.value.district,
		});

		showCheck.value = true;
		toast.success(t("success"));
		emit("close");
	} catch (e) {
		errorHandling(e);
		showX.value = true;
	} finally {
		showSpinningWheel.value = false;
	}
};
</script>
