<template>
	<div v-if="tournament != null">
		<BracketEdit
			v-if="
				tournament.category.category_type.name != 'Tournament' ||
				tournament.matches.length < 33
			"
			:tournament="tournament" />
		<p v-else>
			{{ t("tournament.matchesError") }}
		</p>
	</div>
</template>

<script setup>
import BracketEdit from "@/components/partials/skeletons/bracketEdit.vue";
import { authApi } from "@/services/api";
import { ref } from "vue";
import toast from "@/toast.js";
import { useI18n } from "vue-i18n";

let { t } = useI18n();

const props = defineProps({
	// ID of the competition
	competition: {
		type: String,
		required: true,
	},
	// ID of the tournament
	tournament: {
		type: String,
		required: true,
	},
});

let tournament = ref(null);

authApi
	.get("competitions/" + props.competition + "/tournaments/" + props.tournament)
	.then((response) => {
		tournament.value = response.data;
	})
	.catch(() => {
		toast.error(t("tournament.notLoaded"));
	});
</script>

<i18n>
{
  "en_GB": {
    "tournament": {
		"notLoaded": "Wasn't possible to load the tournament",
		"matchesError": "The tournament has more than 33 matches"
    },
	"table": {
		"name": "Name",
		"matches": "Matches",
		"preview": "Show Tournament"
	}
  },
  "pt_PT": {
  }
}
</i18n>
