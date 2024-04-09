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
							class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle absolute inset-0 overflow-y-auto sm:w-full sm:p-6">
							<Loading v-if="props.tournament == null" />
							<div v-else>
								<div
									v-if="props.tournament.matches.length == 0"
									class="absolute inset-0">
									<div
										class="relative top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 max-w-max">
										<p class="font-medium text-3xl">
											{{ t("error.tournamentNoAthletesSignedUp") }}
										</p>
									</div>
								</div>
								<div
									v-else-if="
										props.tournament.category.category_type.name == 'Tournament'
									"
									:class="[
										'absolute top-0 left-0',
										props.tournament.matches.length > 50
											? 'scale-x-50 scale-y-50 -translate-x-1/4 -translate-y-1/4'
											: '',
									]">
									<Bracket2
										v-if="props.tournament.matches.length < 2"
										:tournament="props.tournament" />
									<Bracket3
										v-else-if="props.tournament.matches.length < 4"
										:tournament="props.tournament" />
									<Bracket4
										v-else-if="props.tournament.matches.length < 5"
										:tournament="props.tournament" />
									<Bracket8
										v-else-if="props.tournament.matches.length < 9"
										:tournament="props.tournament" />
									<Bracket16
										v-else-if="props.tournament.matches.length < 17"
										:tournament="props.tournament" />
									<Bracket32
										v-else-if="props.tournament.matches.length < 33"
										:tournament="props.tournament" />
									<p v-else>
										{{ t("error.tournamentToManyMatches") }}
									</p>
								</div>
								<div v-else class="absolute inset-0">
									<ListTournament :tournament="props.tournament" />
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
import Bracket2 from "@/components/partials/skeletons/bracket2.vue";
import Bracket3 from "@/components/partials/skeletons/bracket3.vue";
import Bracket4 from "@/components/partials/skeletons/bracket4.vue";
import Bracket8 from "@/components/partials/skeletons/bracket8.vue";
import Bracket16 from "@/components/partials/skeletons/bracket16.vue";
import Bracket32 from "@/components/partials/skeletons/bracket32.vue";
import ListTournament from "@/components/partials/skeletons/listTournament.vue";
import Loading from "@/components/partials/loading.vue";
import { Dialog, DialogOverlay, TransitionChild, TransitionRoot } from "@headlessui/vue";
import { ref, watch } from "vue";
import { useI18n } from "vue-i18n";

let { t } = useI18n({ useScope: "global" });

const props = defineProps({
	// Tournament Object
	tournament: {
		type: Object,
		required: true,
	},
	open: {
		type: Boolean,
		required: true,
	},
});
let open = ref(props.open);
const emit = defineEmits(["close"]);
watch(
	() => props.open,
	(after) => {
		open.value = after;
	}
);
</script>
