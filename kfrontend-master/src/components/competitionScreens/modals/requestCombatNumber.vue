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
							<div>
								<p class="text-xl font-semibold text-center mb-4 capitalize">
									{{ t("insertMatchNumber") }}
								</p>
								<form
									@submit.prevent="
										emit('next', state);
										emit('close');
									">
									<CustomInput
										:label="t('nextMatchNumber')"
										type="text"
										:name="'nextMatchNumber'"
										:option-selected="state"
										:error="''"
										@value-changed="(option) => (state = option)" />
								</form>
								<div class="relative w-60 left-1/2 -translate-x-1/2 mt-20">
									<Button
										:type="'primary'"
										:message="t('insertMatchNumber')"
										@button-click="
											emit('next', state);
											emit('close');
										" />
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
import CustomInput from "@/components/partials/inputs/customInput.vue";
import Button from "@/components/partials/button.vue";
import { useI18n } from "vue-i18n";
import { ref, watch } from "vue";

let { t } = useI18n({ useScope: "global" });
let open = ref(false);

const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	number: {
		type: String,
		required: true,
	},
});
const emit = defineEmits(["close", "next"]);

let state = ref("");

watch(
	() => props.open,
	(after) => {
		open.value = after;
		if (after) {
			state.value = (Number(props.number) + 1).toString();
		}
	}
);
</script>
