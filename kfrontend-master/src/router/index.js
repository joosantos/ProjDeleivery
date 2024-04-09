import { createWebHistory, createRouter } from "vue-router";
import store from "@/store";
import toast from "@/toast.js";
import localStorageService from "@/services/localStorage.service";

// Import dos componentes
//#region Import User
import Login from "@/components/user/login.vue";
import Register from "@/components/user/register.vue";
import VerifyEmail from "@/components/user/verifyEmail.vue";
import ForgotPassword from "@/components/user/forgotPassword.vue";
import RecoverPassword from "@/components/user/recoverPassword.vue";
import Block from "@/components/user/block.vue";
import VerifyAdmin from "@/components/user/verifyAdmin.vue";
//#endregion
//#region Import Admin
import VerifyCoaches from "@/components/admin/verifyCoaches.vue";
import AdminDashboard from "@/components/admin/dashboard.vue";
import BlockCoaches from "@/components/admin/blockCoaches.vue";
import Teams from "@/components/admin/teams.vue";
import Athletes from "@/components/admin/athletes.vue";
import AthleteDetails from "@/components/admin/athleteDetails.vue";
import Insurances from "@/components/admin/insurances.vue";
import InsurancesConfig from "@/components/admin/insurancesConfig.vue";
import InsureMultiple from "@/components/admin/insureMultiple.vue";
import Coaches from "@/components/admin/coaches.vue";
import CoachDetails from "@/components/admin/coachDetails.vue";
import TeamDetails from "@/components/admin/teamDetails.vue";
import CreateStickers from "@/components/admin/createStickers.vue";
import AdminFederationRequests from "@/components/admin/federationRequests.vue";
import InsurancesDetails from "@/components/admin/insurancesDetails.vue";
//#endregion
//#region Import Area
import TemplateCombat from "@/components/competitionScreens/publicView.vue";
import TableView from "@/components/competitionScreens/tableView.vue";
//#endregion
//#region Import Competition
import ShowCompetitions from "@/components/competition/showAll.vue";
import CompetitionCreate from "@/components/competition/create.vue";
import CompetitionDetails from "@/components/competition/details.vue";
import OrderTournaments from "@/components/competition/orderTournaments.vue";
import ShowCompetition from "@/components/competition/showCompetition.vue";
import ShowTournament from "@/components/competition/showTournament.vue";
import PrintTournament from "@/components/competition/printTournament.vue";
import EditTournament from "@/components/competition/editTournament.vue";
import Statistics from "@/components/competition/statistics.vue";
import StatisticsAthletesNumbers from "@/components/competition/statisticsAthletesNumbers.vue";
import StatisticsAthlete from "@/components/competition/statisticsAthlete.vue";
import StatisticsTeam from "@/components/competition/statisticsTeam.vue";
import Diploma1 from "@/components/competition/diplomas/diploma1.vue";
import Diploma2 from "@/components/competition/diplomas/diploma2.vue";
import Diploma3 from "@/components/competition/diplomas/diploma3.vue";
import PrintToPdf from "@/components/competition/printToPdf.vue";
import Inscriptions from "@/components/competition/inscriptions.vue";
import InscriptionsNotConfirmed from "@/components/competition/inscriptionsNotConfirmed.vue";
import InscriptionsTeam from "@/components/competition/inscriptionsTeam.vue";
import EditTournaments from "@/components/competition/editTournaments.vue";
import CompetitionTournamentsPrint from "@/components/competition/competitionTournamentsPrint.vue";
import InscriptionEdit from "@/components/competition/inscriptionEdit.vue";
import ShowCombatsByArea from "@/components/competition/showCombatsByArea.vue";
import SeeTimeLeftByArea from "@/components/competition/seeTimeLeftByArea.vue";
import ShowTournamentsByTeam from "@/components/competition/showTournamentsByTeam.vue";
//#endregion
//#region Import Coach
import CoachDashboard from "@/components/coach/dashboard.vue";
import TeamView from "@/components/coach/teamView.vue";
import InsuranceRequestsCreateOrUpdate from "@/components/coach/insuranceRequestsCreateOrUpdate.vue";
import InsuranceRequests from "@/components/coach/insuranceRequests.vue";
import InsuranceRequestDetails from "@/components/coach/insuranceRequestDetails.vue";
//#endregion
//#region Import Athletes
import AthletePage from "@/components/athletes/athletePage.vue";
import GlobalStatistics from "@/components/athletes/globalStatistics.vue";
import AthletesSearch from "@/components/athletes/athletesSearch.vue";
//#endregion
//#region Import Others
import Home from "@/components/home.vue";
import NotFound from "@/components/notFound.vue";
import ChooseCompetition from "@/components/competitionScreens/chooseCompetition.vue";
import MicrophoneView from "@/components/competitionScreens/microphoneView.vue";
import PodiumView from "@/components/competitionScreens/podiumView.vue";
//#endregion

// Definição das routes
const routes = [
	//#region User
	{
		path: "/login",
		name: "Login",
		component: Login,
		meta: { requiresAnnon: true },
	},
	{
		path: "/register",
		name: "Register",
		component: Register,
		meta: { requiresAnnon: true },
	},
	{
		path: "/auth/confirm/:userId?",
		name: "Verify Email",
		component: VerifyEmail,
		meta: { requiresAnnon: true },
		props: true,
	},
	{
		path: "/auth/verify/:refuse",
		name: "Verify Admin",
		component: VerifyAdmin,
		meta: { requiresAnnon: true },
		props: true,
	},
	{
		path: "/blocked",
		name: "Block",
		component: Block,
		meta: { requiresAnnon: true },
		props: true,
	},
	{
		path: "/forgot-password",
		name: "Forgot Password",
		component: ForgotPassword,
		meta: { requiresAnnon: true },
	},
	{
		path: "/recover/password",
		name: "Recover Password",
		component: RecoverPassword,
		meta: { requiresAnnon: true },
	},
	//#endregion
	//#region Area
	{
		path: "/combat/manager",
		name: "Combat Competition",
		component: ChooseCompetition,
		meta: { requiresLogin: true, requiresArea: true },
	},
	{
		path: "/combat",
		name: "Template Combat",
		component: TemplateCombat,
		meta: { requiresLogin: true, requiresArea: true },
	},
	{
		path: "/combat/manager/:competitionId",
		name: "Combat Manager",
		component: TableView,
		meta: { requiresLogin: true, requiresArea: true },
		props: true,
	},
	//#endregion
	//#region Competition
	{
		path: "/competitions",
		name: "Competition",
		component: ShowCompetitions,
	},
	{
		path: "/competition/create",
		name: "Competition Create",
		component: CompetitionCreate,
		meta: { requiresLogin: true, requiresAdmin: true },
	},
	{
		path: "/competitions/:competitionId",
		name: "Competition Details",
		component: CompetitionDetails,
		meta: { requiresLogin: true, requiresAdmin: true },
		props: true,
	},
	{
		path: "/competition/:competitionId/edit",
		name: "Competition Edit Dates",
		component: CompetitionCreate,
		meta: { requiresLogin: true, requiresAdmin: true },
		props: true,
	},
	{
		path: "/competitions/:competitionId/order",
		name: "Order Tournaments",
		component: OrderTournaments,
		meta: { requiresLogin: true, requiresAdmin: true },
		props: true,
	},
	{
		path: "/tournament/print",
		name: "Print Tournament",
		component: PrintTournament,
	},
	{
		path: "/tournaments/:tournament",
		name: "Show Tournament",
		component: ShowTournament,
		props: true,
	},
	{
		path: "/tournaments/edit/:competition/:tournament",
		name: "Edit Tournament",
		component: EditTournament,
		meta: { requiresLogin: true, requiresAdmin: true },
		props: true,
	},
	{
		path: "/competitions/show/:competition",
		name: "Show Competition",
		component: ShowCompetition,
		props: true,
	},
	{
		path: "/competitions/:competition/statistics",
		name: "Statistics",
		component: Statistics,
		props: true,
	},
	{
		path: "/competitions/:competition/athletes-numbers",
		name: "Statistics Athletes Numbers",
		component: StatisticsAthletesNumbers,
		props: true,
	},
	{
		path: "/competitions/:competition/statistics/athlete/:athleteId/:athleteCompetitionId",
		name: "Athlete Statistics",
		component: StatisticsAthlete,
		props: true,
	},
	{
		path: "/competitions/:competition/statistics/team/:team",
		name: "Team Statistics",
		component: StatisticsTeam,
		props: true,
	},
	{
		path: "/diploma1/:tournament/",
		name: "Diploma 1",
		component: Diploma1,
		meta: { requiresLogin: true, requiresPodium: true },
		props: true,
	},
	{
		path: "/diploma2/:tournament/",
		name: "Diploma 2",
		component: Diploma2,
		meta: { requiresLogin: true, requiresPodium: true },
		props: true,
	},
	{
		path: "/diploma3/:tournament/",
		name: "Diploma 3",
		component: Diploma3,
		meta: { requiresLogin: true, requiresPodium: true },
		props: true,
	},
	{
		path: "/competition/:competitionId/print",
		name: "Print Competition",
		component: PrintToPdf,
		meta: { requiresLogin: true, requiresAdmin: true },
		props: true,
	},
	{
		path: "/competition/:competitionId/inscriptions",
		name: "Competition Inscriptions",
		component: Inscriptions,
		meta: { requiresLogin: true, requiresAdmin: true },
		props: true,
	},
	{
		path: "/competition/:competitionId/inscriptions/not-confirmed",
		name: "Competition Inscriptions Not Confirmed",
		component: InscriptionsNotConfirmed,
		meta: { requiresLogin: true, requiresAdmin: true },
		props: true,
	},
	{
		path: "/competition/:competitionId/inscriptions/team/:teamId",
		name: "Inscriptions Team",
		component: InscriptionsTeam,
		meta: { requiresLogin: true, requiresAdmin: true },
		props: true,
	},
	{
		path: "/competition/:competitionId/edit-tournaments",
		name: "Edit Tournaments",
		component: EditTournaments,
		meta: { requiresLogin: true, requiresAdmin: true },
		props: true,
	},
	{
		path: "/competition/:competitionId/tournaments/print",
		name: "Competition Tournaments Print",
		component: CompetitionTournamentsPrint,
		meta: { requiresLogin: true, requiresAdmin: true },
		props: true,
	},
	{
		path: "/inscription/edit/:tournamentId/:athleteCompetitionId",
		name: "Inscription Edit",
		component: InscriptionEdit,
		meta: { requiresLogin: true, requiresAdmin: true },
		props: true,
	},
	{
		path: "/competitions/:competitionId/show-combats",
		name: "Show Combats By Area",
		component: ShowCombatsByArea,
		props: true,
	},
	{
		path: "/competitions/:competitionId/see-time-left",
		name: "See Time Left",
		component: SeeTimeLeftByArea,
		props: true,
		meta: { requiresLogin: true, requiresAdmin: true },
	},
	{
		path: "/competitions/:competitionId/tournaments-by-team",
		name: "Show Tournaments By Team",
		component: ShowTournamentsByTeam,
		props: true,
		meta: { requiresLogin: true, requiresCoach: true },
	},
	//#endregion
	//#region Admin
	{
		path: "/admin/dashboard",
		name: "Admin Dashboard",
		component: AdminDashboard,
		meta: { requiresLogin: true, requiresAdmin: true },
	},
	{
		path: "/admin/verify-coaches",
		name: "Verify Coaches",
		component: VerifyCoaches,
		meta: { requiresLogin: true, requiresAdmin: true },
	},
	{
		path: "/admin/block-coaches",
		name: "Block Coaches",
		component: BlockCoaches,
		meta: { requiresLogin: true, requiresAdmin: true },
	},
	{
		path: "/admin/teams",
		name: "Teams",
		component: Teams,
		meta: { requiresLogin: true, requiresAdmin: true },
	},
	{
		path: "/admin/teams/:teamId/athletes",
		name: "Athletes By Team",
		component: Athletes,
		meta: { requiresLogin: true, requiresAdmin: true },
		props: true,
	},
	{
		path: "/admin/athletes/:athleteId",
		name: "Athlete Details",
		component: AthleteDetails,
		meta: { requiresLogin: true, requiresAdmin: true },
		props: true,
	},
	{
		path: "/admin/insurances",
		name: "Insurances",
		component: Insurances,
		meta: { requiresLogin: true, requiresAdmin: true },
	},
	{
		path: "/admin/insurances/:?insurancesId",
		name: "Insurance Detail",
		component: Insurances,
		meta: { requiresLogin: true, requiresAdmin: true },
		props: true,
	},
	{
		path: "/admin/insurances/group",
		name: "Insurances Group Details",
		component: InsurancesDetails,
		meta: { requiresLogin: true, requiresAdmin: true },
		props: (route) => ({
			paymentComprovativeUrl: route.query.paymentcomprovativeurl,
			insuranceGroup: route.query.insurancegroup,
			insuranceId: route.query.insuranceid,
		}),
	},
	{
		path: "/admin/insurances-config",
		name: "Insurances Config",
		component: InsurancesConfig,
		meta: { requiresLogin: true, requiresAdmin: true },
	},
	{
		path: "/admin/insure-multiple",
		name: "Insure Multiple",
		component: InsureMultiple,
		meta: { requiresLogin: true, requiresAdmin: true },
	},
	{
		path: "/admin/coaches",
		name: "Coaches",
		component: Coaches,
		meta: { requiresLogin: true, requiresAdmin: true },
	},
	{
		path: "/admin/coaches/:coachId",
		name: "Coach Details",
		component: CoachDetails,
		meta: { requiresLogin: true, requiresAdmin: true },
		props: true,
	},
	{
		path: "/admin/teams/:teamId",
		name: "Team Details",
		component: TeamDetails,
		meta: { requiresLogin: true, requiresAdmin: true },
		props: true,
	},
	{
		path: "/admin/stickers",
		name: "Create Stickers",
		component: CreateStickers,
		meta: { requiresLogin: true, requiresAdmin: true },
	},
	{
		path: "/admin/federation-requests",
		name: "Admin Federation Requests",
		component: AdminFederationRequests,
		meta: { requiresLogin: true, requiresAdmin: true },
	},
	{
		path: "/admin/team/:teamId/teamDetails",
		name: "Admin Team View",
		component: TeamView,
		meta: { requiresLogin: true, requiresAdmin: true },
		props: true,
	},
	//#endregion
	//#region Coach
	{
		path: "/coach/dashboard",
		name: "Coach Dashboard",
		component: CoachDashboard,
		meta: { requiresLogin: true, requiresCoach: true },
	},
	{
		path: "/coach/team/:teamId",
		name: "Team View",
		component: TeamView,
		meta: { requiresLogin: true, requiresCoach: true },
		props: true,
	},
	{
		path: "/coach/team/:teamId/athletes/:athleteId",
		name: "Coach Athlete Details",
		component: AthleteDetails,
		meta: { requiresLogin: true, requiresCoach: true },
		props: true,
	},
	{
		path: "/coach/team/:teamId/insurance-requests",
		name: "Insurance Requests",
		component: InsuranceRequests,
		meta: { requiresLogin: true, requiresCoach: true },
		props: true,
	},
	{
		path: "/coach/team/:teamId/insurance-requests/create/:variant",
		name: "Insurance Requests Create",
		component: InsuranceRequestsCreateOrUpdate,
		meta: { requiresLogin: true, requiresCoach: true },
		props: true,
	},
	{
		path: "/coach/team/:teamId/insurance-requests/edit/:insuranceId",
		name: "Insurance Requests Update",
		component: InsuranceRequestsCreateOrUpdate,
		meta: { requiresLogin: true, requiresCoach: true },
		props: true,
	},
	{
		path: "/coach/team/:teamId/insurance-requests/:subTeamGroup",
		name: "Insurance Request Details",
		component: InsuranceRequestDetails,
		meta: { requiresLogin: true, requiresCoach: true },
		props: true,
	},
	//#endregion
	//#region Athletes
	{
		path: "/athletes/:athleteId",
		name: "Athlete Page",
		component: AthletePage,
		props: true,
	},
	{
		path: "/statistics",
		name: "Global Statistics",
		component: GlobalStatistics,
	},
	{
		path: "/athletes",
		name: "Athletes Search",
		component: AthletesSearch,
	},
	//#endregion
	//#region Others
	{ path: "/", name: "Root", component: Home, meta: { isHome: true } },
	{
		path: "/microphone",
		name: "Microphone Competition",
		component: ChooseCompetition,
		meta: { requiresLogin: true, requiresMicrophone: true },
	},
	{
		path: "/microphone/:competitionId",
		name: "Microphone",
		component: MicrophoneView,
		meta: { requiresLogin: true, requiresMicrophone: true },
		props: true,
	},
	{
		path: "/podium",
		name: "Podium Competition",
		component: ChooseCompetition,
		meta: { requiresLogin: true, requiresPodium: true },
	},
	{
		path: "/podium/:competitionId",
		name: "Podium",
		component: PodiumView,
		meta: { requiresLogin: true, requiresPodium: true },
		props: true,
	},
	{ path: "/home", name: "Home", component: Home, meta: { isHome: true } },
	//#endregion
	// Must be last route
	{ path: "/:catchAll(.*)", name: "404", component: NotFound },
];

// Criação do router
const router = createRouter({
	history: createWebHistory(),
	routes,
});

// Verificar se o user tem as condições necessárias para aceder à página
router.beforeResolve(async (to) => {
	const requiresLogin = to.matched.some((record) => record.meta.requiresLogin);
	const requiresAnnon = to.matched.some((record) => record.meta.requiresAnnon);
	const requiresAdmin = to.matched.some((record) => record.meta.requiresAdmin);
	const requiresArea = to.matched.some((record) => record.meta.requiresArea);
	const requiresMicrophone = to.matched.some((record) => record.meta.requiresMicrophone);
	const requiresPodium = to.matched.some((record) => record.meta.requiresPodium);
	const requiresCoach = to.matched.some((record) => record.meta.requiresCoach);
	// const isHome = to.matched.some((record) => record.meta.isHome);

	if (requiresLogin && store.getters.getUser != null) {
		if (localStorageService.getRefreshToken() == null) {
			toast.error("Please log in first.");
			store.commit("setUser", null);
			return { name: "Login" };
		}
	}
	if (requiresLogin && store.getters.getUser == null) {
		// Necessário autenticação para aceder
		toast.error("Please log in first.");
		return { name: "Login" };
	}
	if (requiresAnnon && store.getters.getUser != null) {
		// Necessário não ter autenticação para aceder
		toast.error("You are already logged.");
		return { name: "Home" };
	}
	if (store.getters.getUserRole === "ADMIN") {
		return;
	}
	if (requiresAdmin) {
		toast.error("Only admins can access this page");
		return { name: "Home" };
	}
	if (requiresArea && store.getters.getUserRole != "AREA") {
		toast.error("Only areas can access this page");
		return { name: "Home" };
	}
	if (requiresMicrophone && store.getters.getUserRole != "MICRO") {
		toast.error("Only the Microphone can access this page");
		return { name: "Home" };
	}
	if (requiresPodium && store.getters.getUserRole != "PODIUM") {
		toast.error("Only the Podium can access this page");
		return { name: "Home" };
	}
	if (requiresCoach && store.getters.getUserRole != "COACH") {
		toast.error("Only coaches can access this page");
		return { name: "Home" };
	}
	/*if (!requiresAnnon && store.getters.getUser == null && !isHome) {
		toast.error("Access blocked due to high traffic");
		return { name: "Home" };
	}*/
});

export default router;
