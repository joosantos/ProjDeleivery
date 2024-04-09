<template>
	<div class="hidden">
		<div id="copyListTournaments" ref="copyListHtmlTournaments">
			<div v-for="tournament in props.inscriptionsTournament" :key="tournament.tournament_id">
				<div v-if="tournament.athletes.findIndex((a) => a.accepted) !== -1">
					<h3 class="font-semibold text-lg">
						{{ tournament.name }}
					</h3>
					<div v-for="athlete in tournament.athletes" :key="athlete.athlete_id">
						<p v-if="athlete.accepted">
							{{ `${getAthleteName(athlete.athlete)} (__________)` }}
						</p>
					</div>
					<br />
				</div>
			</div>
		</div>
		<div id="copyListAthletes" ref="copyListHtmlAthletes">
			<div v-for="athlete in inscriptionsAthletes" :key="athlete.athlete_id">
				<div v-if="athlete.tournaments.findIndex((a) => a.accepted) !== -1">
					<h3 class="font-semibold text-lg">
						{{ athlete.name }}
					</h3>
					<div v-for="tournament in athlete.tournaments" :key="tournament.tournament_id">
						<p v-if="tournament.accepted">
							{{ `${tournament.name} (__________)` }}
						</p>
					</div>
					<br />
				</div>
			</div>
		</div>
	</div>
</template>
<script setup>
import { getAthleteName } from "@/services/athlete.service.js";
import { ref, onMounted } from "vue";

const props = defineProps({
	inscriptionsTournament: {
		type: Array,
		required: true,
	},
	inscriptionsAthletes: {
		type: Array,
		required: true,
	},
});
const copyListHtmlAthletes = ref(null);
const copyListHtmlTournaments = ref(null);
const emit = defineEmits(["copyListHtmlAthletes", "copyListHtmlTournaments"]);

onMounted(() => {
	emit("copyListHtmlAthletes", copyListHtmlAthletes.value);
	emit("copyListHtmlTournaments", copyListHtmlTournaments.value);
});
</script>
