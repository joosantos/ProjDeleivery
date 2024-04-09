<template>
	<div class="min-w-max xl:min-w-0">
		<!-- Table Header -->
		<div
			class="grid grid-cols-8 border-2 rounded-3xl border-blue-700 text-center divide-x-2 divide-blue-700 text-2xl font-medium rounded-b-none">
			<div class="col-span-1 p-2">
				<p class="top-1/2 relative -translate-y-1/2">
					{{ t("federated") }}
				</p>
			</div>
			<div class="col-span-1 p-2">
				<p class="top-1/2 relative -translate-y-1/2">
					{{ t("fedNumber") }}
				</p>
			</div>
			<div class="col-span-2 p-2">
				<p class="top-1/2 relative -translate-y-1/2">
					{{ t("name") }}
				</p>
			</div>

			<div class="col-span-1 p-2">
				<p class="top-1/2 relative -translate-y-1/2">
					{{ t("age") }}
				</p>
			</div>

			<div class="col-span-1 p-2">
				<p class="top-1/2 relative -translate-y-1/2">
					{{ t("weight") }}
				</p>
			</div>

			<div class="col-span-1 p-2">
				<p class="top-1/2 relative -translate-y-1/2">
					{{ t("belt") }}
				</p>
			</div>
			<div class="col-span-1 p-2" />
		</div>

		<!-- If Table Empty -->
		<div
			v-if="props.athletes.length == 0"
			class="grid grid-cols-1 grid-rows-2 border-2 border-t-0 border-blue-700 text-center divide-y-2 divide-blue-700 rounded-3xl rounded-t-none">
			<p class="p-2 font-medium text-xl">{{ t("noAthletes") }}</p>
			<router-link
				:to="{
					name: 'Coach Athlete Details',
					params: { teamId: props.teamId, athleteId: '0' },
				}"
				class="p-2 font-medium text-xl inline-flex bg-green-200 text-green-500 hover:bg-green-300 hover:text-green-700 active:bg-green-400 rounded-b-3xl">
				<PlusIcon class="h-7 w-7 ml-auto mr-2" />
				<p class="mr-auto font-medium">
					{{ t("addAthlete") }}
				</p>
			</router-link>
		</div>

		<!-- If Table Not Empty -->
		<div
			v-for="(athlete, idx) of props.athletes"
			:key="athlete.id"
			:class="[
				'grid grid-cols-8 border-2 border-t-0 border-blue-700text-center divide-x-2 divide-blue-700 border-bottom-2 border-blue-700 text-lg font-medium',
				idx == props.athletes.length - 1 && 'rounded-b-3xl',
			]">
			<div class="col-span-1 px-2 py-1 mx-auto">
				<CheckCircleIcon
					v-if="athlete.federated_in_current_season"
					class="h-7 w-7 text-green-500" />
				<XCircleIcon v-else class="h-7 w-7 text-red-500" />
			</div>
			<div class="col-span-1 px-2 py-1">
				{{ athlete.private_info.federation_number }}
			</div>
			<router-link
				:to="{ name: 'Athlete Page', params: { athleteId: athlete.id } }"
				target="_blank"
				class="col-span-2 px-2 py-1 link">
				<div class="inline-flex space-x-2">
					<img
						class="w-10 rounded-full"
						:src="
							athlete.profile_picture_url
								? `https://kempo-files.fra1.digitaloceanspaces.com/${athlete.profile_picture_url}`
								: '/defaultUserImage.png'
						"
						alt="" />
					<p class="">
						{{ athlete.name }}
					</p>
				</div>
			</router-link>
			<div class="col-span-1 px-2 py-1">
				{{ getAge(athlete.birthday) }}
			</div>
			<div class="col-span-1 px-2 py-1">
				{{ athlete.weight }}
			</div>
			<div class="col-span-1 px-2 py-1">
				<p v-if="athlete?.belt?.name">
					{{ t(`belts.${athlete.belt.name}`) }}
				</p>
			</div>
			<div class="col-span-1 2xl:px-2 py-1">
				<div @click.prevent="null" class="inline-flex space-x-4 xl:space-x-1 2xl:space-x-4">
					<Tooltip :text="t('edit')">
						<router-link
							:to="{
								name:
									store.getters.getUserRole === 'ADMIN'
										? 'Athlete Details'
										: 'Coach Athlete Details',
								params:
									store.getters.getUserRole === 'ADMIN'
										? { athleteId: athlete.id }
										: {
												teamId: props.teamId,
												athleteId: athlete.id,
										  },
							}">
							<PencilIcon
								class="w-7 h-7 text-yellow-500 bg-yellow-200 rounded-full p-1 cursor-pointer hover:bg-yellow-400 hover:text-yellow-700" />
						</router-link>
					</Tooltip>
					<Tooltip :text="t('remove')">
						<XMarkIcon
							class="w-7 h-7 text-red-500 bg-red-200 rounded-full p-1 cursor-pointer hover:bg-red-400 hover:text-red-700"
							@click="
								emit('removeAthlete', { id: athlete.id, name: athlete.name })
							" />
					</Tooltip>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import Tooltip from "@/components/partials/templates/tooltip.vue";
import store from "@/store";
import {
	CheckCircleIcon,
	PencilIcon,
	PlusIcon,
	XCircleIcon,
	XMarkIcon,
} from "@heroicons/vue/24/solid";
import { useI18n } from "vue-i18n";

let { t } = useI18n();
const today = new Date();
const emit = defineEmits(["removeAthlete"]);

const props = defineProps({
	teamId: {
		type: String,
		required: true,
	},
	athletes: {
		type: Array,
		required: false,
		default: [],
	},
});

function getAge(birthday) {
	let birthDate = new Date(birthday);
	let age = today.getFullYear() - birthDate.getFullYear();
	let m = today.getMonth() - birthDate.getMonth();
	if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
		age--;
	}
	return age;
}
</script>
