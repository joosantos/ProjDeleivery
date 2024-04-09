<template>
	<CustomModal
		:open="props.open"
		:title="
			t(
				store.getters.getUserRole == 'ADMIN'
					? 'federationRequest.modal.title'
					: 'federationRequest.modal.coachTitle'
			)
		"
		@close="emit('close')">
		<form
			@submit.prevent="store.getters.getUserRole == 'ADMIN' ? sendRequest() : emit('close')">
			<TextAreaInput
				v-if="store.getters.getUserRole == 'ADMIN'"
				:rows="3"
				:label="t('federationRequest.modal.form.denyReason')"
				:name="'denyReason'"
				:option-selected="denyReason"
				:error="''"
				:readonly="store.getters.getUserRole != 'ADMIN'"
				@value-changed="(option) => (denyReason = option)" />

			<div v-else>
				<p class="text-lg">
					<span class="font-semibold"
						>{{ t("federationRequest.modal.denyReason") }}: </span
					>{{ denyReason }}
				</p>
			</div>
			<Button
				class="mt-4"
				:message="
					t(
						store.getters.getUserRole == 'ADMIN'
							? 'federationRequest.modal.form.button'
							: 'federationRequest.modal.form.close'
					)
				"
				:submit="true"
				type="primary"
				@button-click="null" />
		</form>
	</CustomModal>
</template>

<script setup>
import CustomModal from "@/components/partials/templates/customModal.vue";
import TextAreaInput from "@/components/partials/inputs/textAreaInput.vue";
import Button from "@/components/partials/button.vue";
import store from "@/store";
import { ref, watch } from "vue";
import { useI18n } from "vue-i18n";

let { t } = useI18n({ useScope: "global" });
let denyReason = ref("");

const emit = defineEmits(["close", "submit"]);
const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	federationRequestID: {
		type: String,
		required: true,
	},
	reason: {
		type: String,
		required: true,
	},
});

watch(
	() => props.open,
	(after) => {
		open.value = after;
		if (!after) {
			return;
		}
		denyReason.value = props.reason;
	}
);

function sendRequest() {
	emit("submit", props.federationRequestID, denyReason.value);
	emit("close");
}
</script>
