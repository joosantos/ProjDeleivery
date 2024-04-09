from .user import (
    User,
    UserCreate,
    UserUpdate,
    UserRegister,
    Email,
    PasswordChangeIn,
    PasswordIn,
    AthleteToAssociate,
)
from .role import Role, RoleCreate, RoleUpdate
from .user_role import UserRole, UserRoleCreate, UserRoleUpdate
from .team import Team, TeamCreate, TeamUpdate, TeamInDB, TeamAdmin, TeamName
from .athlete import (
    Athlete,
    AthleteCreate,
    AthleteUpdate,
    AthleteAdmin,
    AthletePrivate,
    AthleteCompleteCreate,
    AthletePrivatePage,
    AthleteAdminUpdate,
    AthleteTournaments,
    UserAdmin,
)
from .competition import (
    Competition,
    CompetitionInDBBase,
    CompetitionCreate,
    CompetitionUpdate,
    CompetitionDetails,
    CompetitionNoMatches,
    CompetitionNoMatchesNoInscriptions,
    CompetitionInDBBase,
)
from .tournament import (
    Tournament,
    TournamentCreate,
    TournamentUpdate,
    TournamentNoInscriptions,
    TournamentPage,
    TournamentName,
    TournamentNoMatches,
    TournamentInscriptionsNoMatches,
    RefereesUpdate,
)
from .athlete_competition import (
    AthleteCompetition,
    AthleteCompetitionCreate,
    AthleteCompetitionUpdate,
)
from .match import (
    Match,
    MatchCreate,
    MatchUpdate,
    MatchesTournamentCreate,
    MatchCalls,
    MatchRequestUpdate,
    MatchRequestSpecial,
)
from .category import Category, CategoryCreate, CategoryUpdate, CategoryName
from .geral_schemas import (
    Podium,
    PagedResponse,
    Date,
    ListIds,
    InscriptionPaymentIn,
)
from .insurance_type import InsuranceType, InsuranceTypeCreate, InsuranceTypeUpdate
from .insurance_group import InsuranceGroup, InsuranceGroupCreate, InsuranceGroupUpdate
from .insured_entity import InsuredEntity, InsuredEntityCreate, InsuredEntityUpdate
from .insurance import (
    Insurance,
    InsuranceCreate,
    InsuranceUpdate,
    InsurancePage,
    InsuranceUpdateDatetime,
    InsuranceTeamSubGroup,
    InsuranceCreateDatetime,
    InsuranceUpdateMulti,
    InsuranceCreateMulti,
    InsuranceGroupped,
    InsuranceUpdateMultiStatus,
    InsuranceUpdateMultiGroups,
)
from .category_type import CategoryType, CategoryTypeCreate, CategoryTypeUpdate
from .belt import Belt, BeltCreate, BeltUpdate
from .athlete_group import AthleteGroup, AthleteGroupCreate, AthleteGroupUpdate
from .inscription import (
    Inscription,
    InscriptionCreate,
    InscriptionUpdate,
    InscriptionsTeams,
    InscriptionsTournament,
)
from .address import Address, AddressCreate, AddressUpdate
from .identification_document import (
    IdentificationDocument,
    IdentificationDocumentCreate,
    IdentificationDocumentUpdate,
)
from .insurance_group import InsuranceGroup, InsuranceGroupCreate, InsuranceGroupUpdate
from .insurance_type import InsuranceType, InsuranceTypeCreate, InsuranceTypeUpdate
from .private_info import PrivateInfo, PrivateInfoCreate, PrivateInfoUpdate
from .responsible import Responsible, ResponsibleCreate, ResponsibleUpdate
from .pagination import PaginatedResponse, PageQueries
from .penalization import Penalization, PenalizationCreate, PenalizationUpdate
