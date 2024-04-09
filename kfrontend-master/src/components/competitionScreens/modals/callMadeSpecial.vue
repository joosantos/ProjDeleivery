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
							<p
								v-if="props.match != null"
								class="text-xl font-semibold text-center mb-4 capitalize">
								{{ t(props.match?.isFireman ? "callFireman" : "callCleaning") }}
							</p>
							<div v-if="props.match != null" class="relative">
								<div class="mt-4 mx-auto max-w-min">
									<AmbulanceIcon
										v-if="match.isFireman"
										class="w-[4.5rem] h-[4.5rem] text-red-500" />
									<MopIcon v-else class="w-[4.5rem] h-[4.5rem] text-yellow-500" />
								</div>
								<p class="text-lg font-medium text-center my-4">
									{{
										t("areaNumber", {
											number: props.match.area_to_call,
										})
									}}
								</p>
								<Button
									:type="'primary'"
									:loading="showLoading"
									:show-x="showX"
									:message="t('called', Number(!props.match?.isFireman))"
									@button-click="callMade()" />
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
import AmbulanceIcon from "@/components/icons/ambulance.vue";
import MopIcon from "@/components/icons/mop.vue";
import Button from "@/components/partials/button.vue";
import { useI18n } from "vue-i18n";
import { ref, watch } from "vue";
import { authApi } from "@/services/api";
import toast from "@/toast.js";

const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	match: {
		type: Object,
		required: false,
		default: null,
	},
});

let { t } = useI18n({ useScope: "global" });
let open = ref(props.open);
let showLoading = ref(false);
let showX = ref(false);
const emit = defineEmits(["close", "sent"]);

watch(
	() => props.open,
	(after) => {
		if (after && props.match == null) {
			toast.error(t("notFound.match"));
			emit("close");
			return;
		}
		open.value = after;
	}
);

function callMade() {
	showLoading.value = true;
	showX.value = false;
	let apiObj = props.match.isFireman
		? { call_request_fireman: false }
		: { call_request_clean: false };

	authApi
		.put(`matches/call-made-special/${props.match.id}`, apiObj)
		.then(() => {
			showLoading.value = false;
			emit("sent");
			emit("close");
		})
		.catch((error) => {
			showLoading.value = false;
			showX.value = true;
			toast.error(t("notFound.match"));
			console.error(error);
		});
}
</script>
