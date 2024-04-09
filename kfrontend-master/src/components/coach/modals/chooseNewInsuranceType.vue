<template>
	<Modal
		:open="props.open"
		:outside-click="true"
		:show-x="true"
		size="5xl"
		@close="emit('close')">
		<div
			class="md:inline-flex md:space-y-0 space-y-8 w-full pt-8 pb-16 md:space-x-8 justify-center">
			<div class="max-w-max rounded-3xl bg-gray-200 cursor-pointer hover:bg-gray-400 p-4">
				<router-link
					:to="{
						name: 'Insurance Requests Create',
						params: { teamId: props.teamId, variant: 'team' },
					}">
					<UserIcon class="w-40 mx-auto" />
					<p class="text-2xl font-medium max-w-[14rem] text-center">
						{{ t("requestInsuranceForTeam") }}
					</p>
				</router-link>
			</div>
			<div class="max-w-max rounded-3xl bg-gray-200 cursor-pointer hover:bg-gray-400 p-4">
				<router-link
					:to="{
						name: 'Insurance Requests Create',
						params: { teamId: props.teamId, variant: 'individuals' },
					}">
					<UsersIcon class="w-40 mx-auto" />
					<p class="text-2xl font-medium max-w-[14rem] text-center">
						{{ t("requestInsuranceForIndividuals") }}
					</p>
				</router-link>
			</div>
			<div class="max-w-max rounded-3xl bg-gray-200 cursor-pointer hover:bg-gray-400 p-4">
				<router-link
					:to="{
						name: 'Insurance Requests Create',
						params: { teamId: props.teamId, variant: 'contract' },
					}">
					<ClipboardDocumentListIcon class="w-40 mx-auto" />
					<p class="text-2xl font-medium max-w-[14rem] text-center">
						{{ t("requestInsuranceWithContract") }}
					</p>
				</router-link>
			</div>
		</div>
	</Modal>
</template>

<script setup>
import Modal from "@/components/partials/modal.vue";
import { UserIcon, UsersIcon, ClipboardDocumentListIcon } from "@heroicons/vue/24/solid";
import { useI18n } from "vue-i18n";

let { t } = useI18n({ useScope: "global" });
const emit = defineEmits(["close"]);

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
</script>
