<template>
	<Modal :open="props.open" :outside-click="true" :show-x="true" @close="emit('close')">
		<div class="-mt-8">
			<p class="text-2xl font-medium">
				{{
					props.insuredName
						? t("refuseInsuranceRequestFor", { name: props.insuredName })
						: t("refuseAllInsuranceRequestsSelected")
				}}
			</p>
			<TextAreaInput
				class="mt-4"
				:rows="5"
				:label="t('refuseMotive')"
				:name="'refuseMotive'"
				:option-selected="refuseMotive"
				:error="errorMotive ? t('error.required') : ''"
				@value-changed="(option) => (refuseMotive = option)" />
			<div class="space-x-16 mt-4 mx-auto max-w-max">
				<Button
					class="max-w-max px-8"
					:message="t('cancel')"
					:type="'primary'"
					:pill="true"
					@button-click="emit('close')" />
				<Button
					class="max-w-max px-8"
					:message="t('refuse')"
					:type="'danger'"
					:pill="true"
					@button-click="emitRefuse" />
			</div>
		</div>
	</Modal>
</template>

<script setup>
import Modal from "@/components/partials/modal.vue";
import TextAreaInput from "@/components/partials/inputs/textAreaInput.vue";
import Button from "@/components/partials/button.vue";
import { ref } from "vue";
import { useI18n } from "vue-i18n";

let { t } = useI18n({ useScope: "global" });
const emit = defineEmits(["close", "refuse"]);

const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	insuredName: {
		type: String,
		required: false,
		defalt: "",
	},
});

const refuseMotive = ref("");
const errorMotive = ref(false);

const emitRefuse = () => {
	errorMotive.value = false;
	if (!refuseMotive.value.trim()) {
		errorMotive.value = true;
		return;
	}
	emit("refuse", refuseMotive.value.trim());
};
</script>
