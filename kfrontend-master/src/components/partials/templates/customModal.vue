<template>
	<div>
		<TransitionRoot as="template" :show="open" @close="props.outClickLeave && emit('close')">
			<Dialog as="div" class="fixed z-20 inset-0 overflow-y-auto">
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
						aria-hidden="true">
						&#8203;
					</span>
					<TransitionChild
						as="template"
						enter="ease-out duration-300"
						enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
						enter-to="opacity-100 translate-y-0 sm:scale-100"
						leave="ease-in duration-200"
						leave-from="opacity-100 translate-y-0 sm:scale-100"
						leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
						<div
							class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-show shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full sm:p-6">
							<div class="inline-flex">
								<XCircleIcon
									v-if="props.showX"
									class="w-10 h-10 text-gray-500 absolute top-4 right-6 hover:text-black cursor-pointer"
									@click="emit('close')" />
								<h1 class="text-3xl font-semibold">{{ props.title }}</h1>
							</div>
							<div class="mt-4"><slot></slot></div>
						</div>
					</TransitionChild>
				</div>
			</Dialog>
		</TransitionRoot>
	</div>
</template>

<script setup>
import { Dialog, DialogOverlay, TransitionChild, TransitionRoot } from "@headlessui/vue";
import { XCircleIcon } from "@heroicons/vue/24/outline";

const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	showX: {
		type: Boolean,
		required: false,
		default: true,
	},
	outClickLeave: {
		type: Boolean,
		required: false,
		default: true,
	},
	title: {
		type: String,
		required: false,
		default: "",
	},
});
const emit = defineEmits(["close"]);
</script>
