<template>
	<div class="relative group">
		<slot></slot>
		<div
			class="invisible opacity-0 duration-300 w-full h-full py-1 px-2 group-hover:visible group-hover:opacity-100 rounded-md absolute right-60 z-30 max-w-[80rem]">
			<div class="bg-white rounded-lg top-6 relative">
				<div
					v-if="props.tournament != null && tournament.matches != null"
					class="scale-[0.25]">
					<div v-if="props.tournament?.matches?.length == 0" class="relative bg-white">
						<div
							class="relative top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 max-w-max">
							<p class="font-medium text-3xl">
								{{ t("error.tournamentNoAthletesSignedUp") }}
							</p>
						</div>
					</div>
					<div
						v-else-if="props.tournament.category?.category_type?.name == 'Tournament'"
						:class="[
							'absolute top-0 left-0 bg-white',
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
					<div v-else class="absolute top-0 left-0 bg-white">
						<ListTournament :tournament="props.tournament" />
					</div>
				</div>
			</div>
		</div>
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
import { useI18n } from "vue-i18n";

let { t } = useI18n({ useScope: "global" });

const props = defineProps({
	// Tournament Object
	tournament: {
		type: Object,
		required: true,
	},
});
</script>
