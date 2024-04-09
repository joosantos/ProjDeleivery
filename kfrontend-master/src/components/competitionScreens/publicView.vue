<template>
	<!-- POSTER -->
	<div v-if="state.showPic" class="absolute inset-0 bg-[#F7F7F7] z-50">
		<img src="/cartaz.jpeg" class="h-full mx-auto" />
	</div>
	<div v-else class="absolute inset-0 overflow-hidden bg-gray-200">
		<!-- HEADER -->
		<div class="py-2 px-4">
			<div
				class="w-full text-center border-2 border-black text-3xl font-bold p-4 rounded-full bg-gray-200">
				{{ state.winner === 0 ? state.title || " " : state.winnerDetails.title || " " }}
			</div>
		</div>

		<!-- Show Podium -->
		<ShowPodiumPublic
			v-if="state.showPodium"
			:first-name="state.podium.first"
			:second-name="state.podium.second"
			:third-name="state.podium.third" />

		<!-- ATHLETES -->
		<div v-else-if="state.winner === 0">
			<div v-if="state.isTournament" class="grid grid-cols-2 gap-x-8 h-full">
				<!-- Blue Side -->
				<div class="col-span-1 bg-blue-500 rounded-tr-3xl h-[2000px]">
					<div class="max-w-max mx-auto mt-20">
						<div
							:class="[
								'front-bolf px-10 text-center pb-4 pt-2 bg-blue-100 border-2 border-black w-[800px] rounded-full',
								blueAthlete.isTeam ? 'text-9xl' : 'text-7xl',
							]">
							<p class="mx-10 whitespace-pre-line">
								{{ blueAthlete.name }}
							</p>
						</div>
						<div
							class="text-4xl front-bolf pb-2 pt-1 text-center w-full bg-blue-300 mt-6 border-2 border-black rounded-full">
							<p>{{ blueAthlete.team }}</p>
						</div>
						<div v-if="!state.hideFouls" class="w-min mt-4">
							<p class="text-center text-4xl font-bold text-white">Fouls</p>
							<div
								class="border border-black bg-gray-200 w-28 h-28 relative rounded-xl">
								<p
									class="m-auto w-min text-red-500 font-bold text-8xl top-1/2 -translate-y-1/2 relative">
									{{
										blueAthlete.fouls == null
											? "0"
											: blueAthlete.fouls == 1
											? "W"
											: blueAthlete.fouls == 0
											? blueAthlete.fouls
											: blueAthlete.fouls - 1
									}}
								</p>
							</div>
						</div>
						<div
							v-if="!state.hidePoints"
							class="text-5xl w-min font-bold text-white bottom-36 absolute left-[250px] -translate-x-[20%]">
							<p class="text-center">Points</p>
							<div
								class="border border-black bg-gray-200 w-52 h-52 relative rounded-3xl">
								<p
									class="m-auto w-min text-black font-bold text-[160px] top-1/2 -translate-y-1/2 relative">
									{{ blueAthlete.points || "0" }}
								</p>
							</div>
						</div>
					</div>
				</div>
				<!-- Red Side -->
				<div class="col-span-1 bg-red-500 rounded-tl-3xl">
					<div class="max-w-max mx-auto mt-20">
						<div
							:class="[
								'front-bolf text-center pb-4 pt-2 bg-blue-100 border-2 border-black w-[800px] rounded-full',
								redAthlete.isTeam ? 'text-9xl' : 'text-7xl',
							]">
							<p class="mx-10 whitespace-pre-line">
								{{ redAthlete.name }}
							</p>
						</div>
						<div
							class="text-4xl front-bolf text-center pb-2 pt-1 w-full bg-red-300 mt-6 border-2 border-black rounded-full">
							<p>{{ redAthlete.team }}</p>
						</div>
						<div v-if="!state.hideFouls" class="w-min mt-4 ml-auto">
							<p class="text-center text-4xl font-bold text-white">Fouls</p>
							<div
								class="border border-black bg-gray-200 w-28 h-28 relative rounded-xl">
								<p
									class="m-auto w-min text-red-500 font-bold text-8xl top-1/2 -translate-y-1/2 relative">
									{{
										redAthlete.fouls == null
											? "0"
											: redAthlete.fouls == 1
											? "W"
											: redAthlete.fouls == 0
											? redAthlete.fouls
											: redAthlete.fouls - 1
									}}
								</p>
							</div>
						</div>
						<div
							v-if="!state.hidePoints"
							class="text-5xl w-min font-bold text-white bottom-36 absolute right-[250px] translate-x-[20%]">
							<p class="text-center">Points</p>
							<div
								class="border border-black bg-gray-200 w-52 h-52 relative rounded-3xl">
								<p
									class="m-auto w-min text-black font-bold text-[160px] top-1/2 -translate-y-1/2 relative">
									{{ redAthlete.points || "0" }}
								</p>
							</div>
						</div>
					</div>
				</div>
				<!-- Combat Number -->
				<div
					class="absolute left-1/2 -translate-x-1/2 top-1/2 -translate-y-1/2 mt-16 h-60 w-60 border-2 border-black bg-gray-200 rounded-xl">
					<p class="text-6xl text-center">Match nº</p>
					<p class="text-9xl text-[11rem] text-center font-semibold my-auto">
						{{ state.fight || " " }}
					</p>
				</div>
				<!-- Timer -->
				<TimerView :big-timer="state.hidePoints" />
			</div>
			<div v-else>
				<!-- Red Side -->
				<div class="p-6">
					<div class="grid bg-red-500 rounded-3xl h-screen">
						<div class="max-w-max mx-auto flex flex-col">
							<div class="text-center w-full text-[64px] mb-10">
								<p
									:class="
										Number(state.fight) -
											Number(state.matches[0].number_by_area) >
										2
											? 'opacity-100'
											: 'opacity-0'
									">
									...
								</p>
							</div>
							<div
								v-for="mat of state.matches"
								v-show="canSeeMatch(mat)"
								:key="mat.number_by_area"
								:class="[
									'front-bolf text-center border-2 py-2 border-black rounded-full flex',
									Number(mat.number_by_area) == Number(state.fight)
										? 'text-9xl text-[128px] bg-white w-[1200px] min-h-[170px]'
										: 'text-2xl text-[32px] w-[800px] mx-auto',
									Number(mat.number_by_area) < Number(state.fight)
										? 'bg-gradient-to-r from-zinc-400 via-zinc-300 to-zinc-200'
										: Number(mat.number_by_area) > Number(state.fight) &&
										  'bg-gradient-to-r from-red-200 via-red-100 to-red-200',
								]">
								<p
									:class="[
										'my-auto mx-4 tabular-nums',
										Number(mat.number_by_area) == Number(state.fight)
											? 'text-[64px]'
											: 'text-[24px]',
									]">
									{{ mat.number_by_area }}
								</p>
								<p
									:class="
										Number(mat.number_by_area) == Number(state.fight)
											? [
													'text-center w-full whitespace-pre-line',
													redAthlete.isTeam
														? 'line-clamp-4 text-6xl text-[80px]'
														: 'line-clamp-2',
											  ]
											: 'line-clamp-1'
									">
									{{
										Number(mat.number_by_area) == Number(state.fight)
											? `${
													redAthlete.isTeam
														? redAthlete.name
														: redAthlete.name.replace("\n", " ")
											  } (${redAthlete.team})\n`
											: `${mat.athlete_red} (${mat.team_red?.toUpperCase()})`
									}}
								</p>
								<p
									v-if="Number(mat.number_by_area) == Number(state.fight)"
									class="my-auto mx-4 tabular-nums text-[64px] opacity-0">
									000
								</p>
								<p
									v-if="Number(mat.number_by_area) < Number(state.fight)"
									class="ml-auto mx-4 tabular-nums">
									{{ formatPoints(mat.points_red) }}
								</p>
							</div>
							<div class="text-center w-full text-[64px]">
								<p
									:class="
										Number(
											state.matches[state.matches.length - 1].number_by_area
										) -
											Number(state.fight) >
										3
											? 'opacity-100'
											: 'opacity-0'
									">
									...
								</p>
							</div>
						</div>
					</div>
				</div>

				<!-- Combat Number -->
				<div
					class="absolute left-1/2 -translate-x-1/2 bottom-14 h-60 w-60 border-2 border-black bg-gray-200 rounded-xl">
					<p class="text-6xl text-center">Match nº</p>
					<p class="text-9xl text-[11rem] text-center font-semibold my-auto">
						{{ state?.fight == null ? " " : state.fight }}
					</p>
				</div>
			</div>
		</div>

		<!-- WIN SCREEN -->
		<WinScreen
			v-else
			:is-red="state.winner === 1"
			:name="state.winnerDetails.name"
			:team="state.winnerDetails.name"
			:match="state.winnerDetails.match" />
	</div>
</template>

<script setup>
import ShowPodiumPublic from "@/components/competitionScreens/partials/publicView/showPodium.vue";
import WinScreen from "@/components/competitionScreens/partials/publicView/winScreen.vue";
import TimerView from "@/components/competitionScreens/partials/publicView/timerView.vue";
import store from "@/store";
import { ref } from "vue";

store.commit("setShowNavBar", false);

let athletesInfo = ref(JSON.parse(localStorage.getItem("tournamentAthletesInfo")) || {});
let redAthlete = ref({
	name:
		athletesInfo.value.athletes.red.name.indexOf(",") !== -1 || false
			? athletesInfo.value.athletes.red.name?.replaceAll(", ", ",\n") || " "
			: athletesInfo.value.athletes.red.name?.replaceAll(" ", ",\n") || " ",
	team: athletesInfo.value.athletes.red.team || " ",
	isTeam: athletesInfo.value.athletes.red.name.indexOf(",") !== -1 || false,
	fouls: athletesInfo.value.athletes.red.fouls || 0,
	points: athletesInfo.value.athletes.red.points || 0,
});
let blueAthlete = ref({
	name: " ",
	team: " ",
	isTeam: false,
	fouls: 0,
	points: 0,
});

let state = ref(JSON.parse(localStorage.getItem("combatDetails")) || {});
if (state.value == null) {
	state.value = { winner: 0 };
}

setInterval(function () {
	state.value = JSON.parse(localStorage.getItem("combatDetails"));
	athletesInfo.value = JSON.parse(localStorage.getItem("tournamentAthletesInfo")) || {};
	updateAthletes();
	if (state.value == null) {
		state.value = { winner: 0 };
		return;
	}
}, 100);

function updateAthletes() {
	redAthlete.value = {
		name:
			athletesInfo.value?.athletes?.red?.name?.indexOf(",") !== -1 || false
				? athletesInfo.value?.athletes?.red?.name?.replaceAll(", ", ",\n") || " "
				: athletesInfo.value?.athletes?.red?.name?.replaceAll(" ", "\n"),
		team: athletesInfo.value?.athletes?.red?.team || " ",
		isTeam: athletesInfo.value?.athletes?.red?.name?.indexOf(",") !== -1 || false,
		fouls: athletesInfo.value?.athletes?.red?.fouls || 0,
		points: athletesInfo.value?.athletes?.red?.points || 0,
	};
	if (!state.value.isTournament) {
		return;
	}
	blueAthlete.value = {
		name:
			athletesInfo.value?.athletes?.blue?.name?.indexOf(",") !== -1 || false
				? athletesInfo.value?.athletes?.blue?.name?.replaceAll(", ", ",\n") || " "
				: athletesInfo.value?.athletes?.blue?.name?.replaceAll(" ", "\n"),
		team: athletesInfo.value?.athletes?.blue?.team || " ",
		isTeam: athletesInfo.value?.athletes?.blue?.name.indexOf(",") !== -1 || false,
		fouls: athletesInfo.value?.athletes?.blue?.fouls || 0,
		points: athletesInfo.value?.athletes?.blue?.points || 0,
	};
}

function canSeeMatch(mat) {
	let matNumber = Number(mat.number_by_area);
	let actualCombat = Number(state.value.fight);

	if (Math.abs(actualCombat - matNumber) <= 3) return true;
	if (matNumber - actualCombat == 4) return true;

	return false;
}

function formatPoints(points) {
	if (!points) return "00.00";

	return Number(points).toFixed(2);
}
</script>
