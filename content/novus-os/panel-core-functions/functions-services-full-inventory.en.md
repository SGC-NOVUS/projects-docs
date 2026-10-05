---
id: panel-core-functions-services-full-inventory
cluster: novus-os
category: panel-core-functions
order: 100
status: active
version: 0.1.0
title: Services Full Inventory
description: Auto-generated inventory of app/Services classes/interfaces/traits and
  their public methods.
last_updated: '2026-10-05'
source_locale: en
locale: en
source_repo: SGC-NOVUS/panel-core
source_branch: main
source_path: docs/functions/services_full_inventory.md
managed_by: sync_private_docs
---
# Services Full Inventory

Auto-generated inventory of app/Services classes/interfaces/traits and their public methods.

- Source: app/Services
- Total entries: 213

## App\Services\Access\ApiKeyService

- Kind: class
- File: app/Services/Access/ApiKeyService.php
- Public methods: __construct(), generate(), validate(), listForUser(), revoke(), delete()

## App\Services\Access\ApiKeyValidatorInterface

- Kind: interface
- File: app/Services/Access/ApiKeyValidatorInterface.php
- Public methods: validate()

## App\Services\Access\AuthService

- Kind: class
- File: app/Services/Access/AuthService.php
- Public methods: __construct(), login(), me(), logout()

## App\Services\Access\IamService

- Kind: class
- File: app/Services/Access/IamService.php
- Public methods: __construct(), overview(), role(), createRole(), updateRole(), deleteRole(), togglePermission()

## App\Services\Access\IdentityIntegrationInterface

- Kind: interface
- File: app/Services/Access/IdentityIntegrationInterface.php
- Public methods: apply()

## App\Services\Access\IdentityProvisioningConsumer

- Kind: class
- File: app/Services/Access/IdentityProvisioningConsumer.php
- Public methods: __construct(), handleProvisioned(), handleLifecycle()

## App\Services\Access\IdentityProvisioningService

- Kind: class
- File: app/Services/Access/IdentityProvisioningService.php
- Public methods: __construct(), emitForIdentity()

## App\Services\Access\OimPolicyGroupService

- Kind: class
- File: app/Services/Access/OimPolicyGroupService.php
- Public methods: __construct(), overview(), group(), createGroup(), updateGroup(), deleteGroup(), togglePolicy(), toggleRoleMapping()

## App\Services\Access\OwnershipGuard

- Kind: class
- File: app/Services/Access/OwnershipGuard.php
- Public methods: __construct(), isAdmin(), canAccess(), listFilterClause()

## App\Services\Access\PermissionService

- Kind: class
- File: app/Services/Access/PermissionService.php
- Public methods: __construct(), can(), policy(), manifest(), require()

## App\Services\Access\RequestAccessService

- Kind: class
- File: app/Services/Access/RequestAccessService.php
- Public methods: __construct(), resolveActor(), authorizeAny(), resolveAcl()

## App\Services\Access\RoleTemplateService

- Kind: class
- File: app/Services/Access/RoleTemplateService.php
- Public methods: __construct(), manifestForRoles(), policyForRoles(), expandRoles()

## App\Services\Access\SshKeyService

- Kind: class
- File: app/Services/Access/SshKeyService.php
- Public methods: __construct(), listForUser(), add(), delete()

## App\Services\Access\VfsAccessPolicy

- Kind: class
- File: app/Services/Access/VfsAccessPolicy.php
- Public methods: __construct(), effectiveRoots(), listRules(), createRule(), deleteRule()

## App\Services\Agent\NovusAgentClient

- Kind: class
- File: app/Services/Agent/NovusAgentClient.php
- Public methods: __construct(), isAvailable(), localAgentId(), registerNode(), health(), updateAgent(), dockerVersion(), dockerInfo(), dockerPing(), listContainers(), inspectContainer(), createContainer(), createInstance(), removeContainer(), listImages(), removeImage(), containerStats(), containerLogs(), pullImage(), resolveRegistryAuthForRef(), powerAction(), pruneDocker(), discoverContainers(), request(), issueToken()

## App\Services\Backups\AgentBackupService

- Kind: class
- File: app/Services/Backups/AgentBackupService.php
- Public methods: __construct(), enqueueCreate(), enqueueRestore(), enqueueDelete()

## App\Services\Backups\BackupPlanService

- Kind: class
- File: app/Services/Backups/BackupPlanService.php
- Public methods: __construct(), list(), get(), create(), update(), delete(), execute(), applyRetention()

## App\Services\Backups\BackupRuntimeService

- Kind: class
- File: app/Services/Backups/BackupRuntimeService.php
- Public methods: __construct(), snapshot(), createSite(), createDb(), delete(), restoreSite(), restoreDb()

## App\Services\Backups\BackupsService

- Kind: class
- File: app/Services/Backups/BackupsService.php
- Public methods: __construct(), snapshot(), createSite(), createDb(), delete(), restoreSite(), restoreDb(), listInstance(), createInstance(), restoreInstance(), enforceGlobalRetention()

## App\Services\Backups\DriveUploader

- Kind: class
- File: app/Services/Backups/DriveUploader.php
- Public methods: __construct(), isConfigured(), upload()

## App\Services\Backups\InstanceBackupEnhancementService

- Kind: class
- File: app/Services/Backups/InstanceBackupEnhancementService.php
- Public methods: __construct(), assertNotThrottled(), lock(), isLocked(), assertNotLocked(), generateSignedDownloadUrl(), validateSignedToken(), recordBackup(), listBackups()

## App\Services\Backups\SudoBackups

- Kind: class
- File: app/Services/Backups/SudoBackups.php
- Public methods: __construct(), listAll(), totalUsageBytes(), delete(), backupSite(), backupDb(), restoreSite(), restoreDb(), listInstance(), backupInstance(), restoreInstance()

## App\Services\Bots\TelegramBotApiService

- Kind: class
- File: app/Services/Bots/TelegramBotApiService.php
- Public methods: __construct(), state(), saveConfig(), testConnection(), getMe(), updateProfile(), getCommands(), setCommands(), getWebhookInfo(), setWebhook(), deleteWebhook(), createInvoiceLink(), sendInvoice(), answerPreCheckoutQuery(), refundStarPayment(), getUpdates(), rawCall()

## App\Services\Branding\BrandingService

- Kind: class
- File: app/Services/Branding/BrandingService.php
- Public methods: __construct(), current(), defaults(), updateTheme(), updateTitleTemplate(), updatePanelName(), uploadAsset(), clearAsset()

## App\Services\Dashboard\DashboardNodeContextService

- Kind: class
- File: app/Services/Dashboard/DashboardNodeContextService.php
- Public methods: __construct(), resolveRemoteContext()

## App\Services\Dashboard\DashboardNodesService

- Kind: class
- File: app/Services/Dashboard/DashboardNodesService.php
- Public methods: __construct(), buildNodes()

## App\Services\Dashboard\DashboardSummaryService

- Kind: class
- File: app/Services/Dashboard/DashboardSummaryService.php
- Public methods: __construct(), dockerSummary(), buildSummary()

## App\Services\Dashboard\DashboardTasksFeedService

- Kind: class
- File: app/Services/Dashboard/DashboardTasksFeedService.php
- Public methods: __construct(), build()

## App\Services\Dashboard\DashboardUpdateCheckService

- Kind: class
- File: app/Services/Dashboard/DashboardUpdateCheckService.php
- Public methods: githubLatestCommit()

## App\Services\Database\BlindIndexQueryBuilder

- Kind: class
- File: app/Services/Database/BlindIndexQueryBuilder.php
- Public methods: __construct(), where(), whereIn(), orderBy(), limit(), get(), first(), insertSensitive()

## App\Services\Database\ConnectionManager

- Kind: class
- File: app/Services/Database/ConnectionManager.php
- Public methods: __construct(), connection(), pdo(), mysqli(), normalizeParams(), fetchAll(), fetchOne(), execute(), close()

## App\Services\Database\DatabaseHelper

- Kind: class
- File: app/Services/Database/DatabaseHelper.php
- Public methods: normalizeParams(), normalizeValue(), boolToSql(), sqlToBool()

## App\Services\Database\DatabaseManager

- Kind: class
- File: app/Services/Database/DatabaseManager.php
- Public methods: __construct(), listDatabases(), listTables(), listUsers(), userGrants(), createDatabase(), dropDatabase(), createUser(), changePassword(), dropUser(), grant(), revokeAll(), flushPrivileges(), exportDatabase()

## App\Services\Database\DatabaseMigrationService

- Kind: class
- File: app/Services/Database/DatabaseMigrationService.php
- Public methods: __construct(), preview(), migrate()

## App\Services\Database\DistributedDatabaseService

- Kind: class
- File: app/Services/Database/DistributedDatabaseService.php
- Public methods: __construct(), listDatabases(), listTables(), listUsers(), userGrants(), listNodeMappings()

## App\Services\Database\EncryptsSensitiveData

- Kind: trait
- File: app/Services/Database/EncryptsSensitiveData.php
- Public methods: 

## App\Services\Eventing\EventBusInterface

- Kind: interface
- File: app/Services/Eventing/EventBusInterface.php
- Public methods: emit(), publish(), pop(), acknowledge(), reject()

## App\Services\Eventing\EventDispatcher

- Kind: class
- File: app/Services/Eventing/EventDispatcher.php
- Public methods: __construct(), dispatch()

## App\Services\Eventing\EventMessage

- Kind: class
- File: app/Services/Eventing/EventMessage.php
- Public methods: __construct(), create(), fromArray(), withAttempt(), toArray()

## App\Services\Eventing\EventWorkerHealthService

- Kind: class
- File: app/Services/Eventing/EventWorkerHealthService.php
- Public methods: __construct(), record(), snapshot(), check()

## App\Services\Eventing\RedisEventBus

- Kind: class
- File: app/Services/Eventing/RedisEventBus.php
- Public methods: __construct(), emit(), publish(), recent(), stats(), pop(), acknowledge(), reject()

## App\Services\Eventing\WebhookService

- Kind: class
- File: app/Services/Eventing/WebhookService.php
- Public methods: __construct(), list(), get(), create(), update(), delete(), dispatchEvent(), subscribe()

## App\Services\Identity\ActivityTimelineService

- Kind: class
- File: app/Services/Identity/ActivityTimelineService.php
- Public methods: __construct(), record(), forUser()

## App\Services\Identity\AuthService

- Kind: class
- File: app/Services/Identity/AuthService.php
- Public methods: __construct(), login(), loginLinkedIdentity(), issueImpersonationSession(), me(), logout()

## App\Services\Identity\MfaVerificationService

- Kind: class
- File: app/Services/Identity/MfaVerificationService.php
- Public methods: __construct(), authenticators(), strongMethods(), registerAuthenticator(), removeAuthenticator(), resetUserAuthenticators(), enrollmentPacket(), challenge(), verify(), requiredMethodsForRoles(), satisfiesRolePolicy(), markSessionAssurance(), sessionStepUpState()

## App\Services\Identity\PermissionOrderService

- Kind: class
- File: app/Services/Identity/PermissionOrderService.php
- Public methods: __construct(), list(), submit(), approve(), deny()

## App\Services\Identity\ProfileService

- Kind: class
- File: app/Services/Identity/ProfileService.php
- Public methods: __construct(), get(), getSteamId(), update(), changeUsername(), uploadAvatar(), clearAvatar(), syncFromSocialProfile(), markBirthdayGrant(), birthdayCandidates(), getUserPasswordHash(), listSsoServices(), revokeSsoService()

## App\Services\Identity\SocialAuthFlowService

- Kind: class
- File: app/Services/Identity/SocialAuthFlowService.php
- Public methods: __construct(), redirect(), callback(), unlink()

## App\Services\Identity\SocialAuthIdentitySummaryService

- Kind: class
- File: app/Services/Identity/SocialAuthIdentitySummaryService.php
- Public methods: identitySummary()

## App\Services\Identity\SocialAuthProfileResolverService

- Kind: class
- File: app/Services/Identity/SocialAuthProfileResolverService.php
- Public methods: __construct(), oauthProfile(), telegramProfile(), steamProfile()

## App\Services\Identity\SocialAuthRedirectUrlService

- Kind: class
- File: app/Services/Identity/SocialAuthRedirectUrlService.php
- Public methods: buildRedirectUrl()

## App\Services\Identity\SocialAuthService

- Kind: class
- File: app/Services/Identity/SocialAuthService.php
- Public methods: __construct(), providers(), isConfigured(), begin(), handleCallback(), linkIdentity(), provisionRestrictedUser(), identities(), unlinkIdentity(), externalIdentityForUser(), findLinkedUserId()

## App\Services\Identity\SocialAuthStateStoreService

- Kind: class
- File: app/Services/Identity/SocialAuthStateStoreService.php
- Public methods: __construct(), storeState(), consumeState()

## App\Services\Identity\SocialAuthTransportService

- Kind: class
- File: app/Services/Identity/SocialAuthTransportService.php
- Public methods: httpJson(), httpForm()

## App\Services\Identity\SocialProfileNormalizerService

- Kind: class
- File: app/Services/Identity/SocialProfileNormalizerService.php
- Public methods: normalize()

## App\Services\Identity\UserLifecycleStateService

- Kind: class
- File: app/Services/Identity/UserLifecycleStateService.php
- Public methods: initialStateForRole(), roleChangeState(), toggleStatus(), statusAfterPasswordSet()

## App\Services\Identity\UserViewBuilderService

- Kind: class
- File: app/Services/Identity/UserViewBuilderService.php
- Public methods: buildListEntry(), buildDetailEntry()

## App\Services\Identity\UsersService

- Kind: class
- File: app/Services/Identity/UsersService.php
- Public methods: __construct(), list(), get(), create(), setRole(), toggleActive(), resetTotp(), sessionsOf(), revokeAllSessions(), revokeOtherSessions(), revokeSingleSession(), rolesOf(), revokeSession(), recentAudit(), recentSecurityEvents(), setPassword(), logAudit(), resolveNidId()

## App\Services\Ims\IncidentService

- Kind: class
- File: app/Services/Ims/IncidentService.php
- Public methods: __construct(), formatId(), slaHoursByImpact(), normalizeLang(), normalizeDateTimeUtc(), validatePayload(), list(), get(), stats(), create(), update(), close(), delete()

## App\Services\Infrastructure\AgentCommandService

- Kind: class
- File: app/Services/Infrastructure/AgentCommandService.php
- Public methods: __construct(), enqueue(), pull(), acknowledge()

## App\Services\Infrastructure\AgentControlDispatchService

- Kind: class
- File: app/Services/Infrastructure/AgentControlDispatchService.php
- Public methods: __construct(), queueContainerStart(), queueContainerStop(), queueContainerRestart(), queueContainerKill(), queueBackupCreate()

## App\Services\Infrastructure\AgentDirectoryService

- Kind: class
- File: app/Services/Infrastructure/AgentDirectoryService.php
- Public methods: __construct(), normalizeDirectoryRows(), normalizeAgentRow(), mergeAgentMeta(), resolveNodePublicId(), getMeta(), isUpdateAvailable(), healthFromLastSeen(), resolvePanelUrl(), defaultAgentIdFromHost(), resolveFrontendAgentId()

## App\Services\Infrastructure\AgentGhcrSecretService

- Kind: class
- File: app/Services/Infrastructure/AgentGhcrSecretService.php
- Public methods: __construct(), resolve()

## App\Services\Infrastructure\AgentHeartbeatService

- Kind: class
- File: app/Services/Infrastructure/AgentHeartbeatService.php
- Public methods: __construct(), touch()

## App\Services\Infrastructure\AgentHttpClientService

- Kind: class
- File: app/Services/Infrastructure/AgentHttpClientService.php
- Public methods: __construct(), isAvailable(), callVfsCommand(), callContainerFsCommand(), probeAgent(), request()

## App\Services\Infrastructure\AgentInstallerService

- Kind: class
- File: app/Services/Infrastructure/AgentInstallerService.php
- Public methods: __construct(), installLocal(), installRemote(), targetVersion()

## App\Services\Infrastructure\AgentNodeActionService

- Kind: class
- File: app/Services/Infrastructure/AgentNodeActionService.php
- Public methods: __construct(), deleteNode(), queueNodeAction()

## App\Services\Infrastructure\AgentProvisioningService

- Kind: class
- File: app/Services/Infrastructure/AgentProvisioningService.php
- Public methods: __construct(), installLocal(), installRemote(), registerNode(), updateMeta(), runtimeTest()

## App\Services\Infrastructure\AgentService

- Kind: class
- File: app/Services/Infrastructure/AgentService.php
- Public methods: __construct(), sharedSecret(), clockSkewSeconds(), issueTokens(), refresh(), revokeRefresh(), verifyAccessToken(), verifyIngressSignature()

## App\Services\Infrastructure\AgentUpdateService

- Kind: class
- File: app/Services/Infrastructure/AgentUpdateService.php
- Public methods: getLatestRelease(), getLatestVersion()

## App\Services\Infrastructure\ConnectionService

- Kind: class
- File: app/Services/Infrastructure/ConnectionService.php
- Public methods: __construct(), touchAgent(), getAgent(), getAgentSecret(), removeAgent(), listAgents(), migrateLegacyStateFromFiles()

## App\Services\Infrastructure\MapIconService

- Kind: class
- File: app/Services/Infrastructure/MapIconService.php
- Public methods: __construct(), upload(), suggestViaIssue(), isAutoUploadAvailable()

## App\Services\Infrastructure\MatrixManifestService

- Kind: class
- File: app/Services/Infrastructure/MatrixManifestService.php
- Public methods: __construct(), normalizeTypeToken(), resolveManifestType(), inferRuntimeFromSignals(), inferTypeFromSignals(), defaultImageForSlug(), resolveManifestImage(), manifestDisplayName(), manifestAuthor(), manifestDescription(), manifestRuntime(), manifestStartupCommand(), manifestVariables(), localizeManifest()

## App\Services\Infrastructure\MatrixSyncService

- Kind: class
- File: app/Services/Infrastructure/MatrixSyncService.php
- Public methods: setAclContext(), __construct(), pull(), diff(), upsertManifest(), exportManifest(), status(), repositoryCatalog(), profile(), deleteMatrix(), updateCustom()

## App\Services\Infrastructure\NovusAgent\GrpcRawStub

- Kind: class
- File: app/Services/Infrastructure/NovusAgent/GrpcRawStub.php
- Public methods: __construct(), unary(), bidi(), serverStream()

## App\Services\Infrastructure\NovusAgent\NovusAgentDirectDriver

- Kind: class
- File: app/Services/Infrastructure/NovusAgent/NovusAgentDirectDriver.php
- Public methods: __construct(), connectionType(), request(), dockerPing(), dockerVersion(), dockerInfo(), listContainers(), inspectContainer(), containerStats(), createContainer(), createInstance(), removeContainer(), telemetry(), dockerAction(), rotateMasterSecret(), pairNode(), unclaimNode(), updateAgent(), ptyStream()

## App\Services\Infrastructure\NovusAgent\NovusAgentDriverInterface

- Kind: interface
- File: app/Services/Infrastructure/NovusAgent/NovusAgentDriverInterface.php
- Public methods: connectionType(), request(), dockerPing(), dockerVersion(), dockerInfo(), telemetry(), listContainers(), inspectContainer(), containerStats(), createContainer(), createInstance(), removeContainer(), dockerAction(), rotateMasterSecret(), pairNode(), unclaimNode(), updateAgent(), ptyStream()

## App\Services\Infrastructure\NovusAgent\NovusAgentFactory

- Kind: class
- File: app/Services/Infrastructure/NovusAgent/NovusAgentFactory.php
- Public methods: __construct(), forNode()

## App\Services\Infrastructure\NovusAgent\NovusAgentFederatedDriver

- Kind: class
- File: app/Services/Infrastructure/NovusAgent/NovusAgentFederatedDriver.php
- Public methods: __construct(), connectionType(), request(), dockerPing(), dockerVersion(), dockerInfo(), telemetry(), listContainers(), inspectContainer(), containerStats(), createContainer(), createInstance(), removeContainer(), dockerAction(), rotateMasterSecret(), pairNode(), unclaimNode(), updateAgent(), ptyStream()

## App\Services\Infrastructure\NovusAgent\NovusProtobufCodec

- Kind: class
- File: app/Services/Infrastructure/NovusAgent/NovusProtobufCodec.php
- Public methods: encode(), decode()

## App\Services\Infrastructure\NovusAgent\RawGrpcMessage

- Kind: class
- File: app/Services/Infrastructure/NovusAgent/RawGrpcMessage.php
- Public methods: __construct(), serializeToString(), decode(), mergeFromString(), bytes()

## App\Services\Infrastructure\NovusAgent\VfsOperationsTrait

- Kind: trait
- File: app/Services/Infrastructure/NovusAgent/VfsOperationsTrait.php
- Public methods: 

## App\Services\Infrastructure\ServerService

- Kind: class
- File: app/Services/Infrastructure/ServerService.php
- Public methods: __construct(), requestContainerStart(), requestContainerStop(), requestContainerRestart(), requestContainerKill(), handleContainerStart(), handleContainerStop(), handleContainerRestart(), handleContainerKill()

## App\Services\Infrastructure\ServiceControlPlaneService

- Kind: class
- File: app/Services/Infrastructure/ServiceControlPlaneService.php
- Public methods: __construct(), queueAgentCommand(), queueLocalAgentCommand()

## App\Services\Integrations\CloudflareDnsService

- Kind: class
- File: app/Services/Integrations/CloudflareDnsService.php
- Public methods: __construct(), isAvailable(), resolveZoneId(), listZones(), createRecord(), upsertRecord(), listRecords(), findRecord(), updateRecord(), deleteRecord(), ensureARecord(), ensureCnameRecord(), ensureWildcardRecord()

## App\Services\Integrations\GeminiConfigResolver

- Kind: class
- File: app/Services/Integrations/GeminiConfigResolver.php
- Public methods: resolveApiKey(), resolveModel()

## App\Services\Integrations\GitHubApiClient

- Kind: class
- File: app/Services/Integrations/GitHubApiClient.php
- Public methods: __construct(), get(), put(), head(), getFileMeta()

## App\Services\Integrations\GitHubTokenResolver

- Kind: class
- File: app/Services/Integrations/GitHubTokenResolver.php
- Public methods: resolve()

## App\Services\Integrations\IntegrationDiagnosticsService

- Kind: class
- File: app/Services/Integrations/IntegrationDiagnosticsService.php
- Public methods: __construct(), probe(), liveTest(), readSecret(), readString()

## App\Services\Integrations\IntegrationProviderService

- Kind: class
- File: app/Services/Integrations/IntegrationProviderService.php
- Public methods: __construct(), cards(), health(), saveProvider(), testProvider()

## App\Services\Integrations\SetupProviderVerificationClient

- Kind: class
- File: app/Services/Integrations/SetupProviderVerificationClient.php
- Public methods: verifyTelegramBotToken(), verifyCloudflareApiToken()

## App\Services\Loader\LoaderProjectService

- Kind: class
- File: app/Services/Loader/LoaderProjectService.php
- Public methods: __construct(), listForTenant(), findById(), create(), archive(), activate()

## App\Services\Loader\LoaderShortlinkConfig

- Kind: class
- File: app/Services/Loader/LoaderShortlinkConfig.php
- Public methods: __construct(), baseDomain(), subdomain(), publicTargetIp(), redirectStatus(), buildPublicUrl(), plannedDnsRecords()

## App\Services\Loader\LoaderTranscodeService

- Kind: class
- File: app/Services/Loader/LoaderTranscodeService.php
- Public methods: __construct(), enqueueFor(), reportFromAgent()

## App\Services\Loader\SftpAccessService

- Kind: class
- File: app/Services/Loader/SftpAccessService.php
- Public methods: __construct(), grant(), revoke(), listForProject()

## App\Services\Loader\ShortlinkService

- Kind: class
- File: app/Services/Loader/ShortlinkService.php
- Public methods: __construct(), create(), resolve(), recordHit(), listForTenant()

## App\Services\Monitoring\A2sQueryService

- Kind: class
- File: app/Services/Monitoring/A2sQueryService.php
- Public methods: query(), queryPlayers()

## App\Services\Monitoring\InfluxTelemetryService

- Kind: class
- File: app/Services/Monitoring/InfluxTelemetryService.php
- Public methods: __construct(), isEnabled(), report(), ensureProvisioned(), renderNativeDeployment(), writeNativeDeployment(), writeMetrics(), writeLog(), latestAgentSnapshot(), metricSeries()

## App\Services\Monitoring\MonitoringIncidentAiService

- Kind: class
- File: app/Services/Monitoring/MonitoringIncidentAiService.php
- Public methods: __construct(), generate()

## App\Services\Monitoring\MonitoringService

- Kind: class
- File: app/Services/Monitoring/MonitoringService.php
- Public methods: __construct(), listTargets(), createTarget(), getTarget(), deleteTarget(), history(), tick(), probeOne(), validateTarget()

## App\Services\Monitoring\PublicStatusPageService

- Kind: class
- File: app/Services/Monitoring/PublicStatusPageService.php
- Public methods: __construct(), ensureDefaultPage(), listPages(), savePage(), publishIncident(), getPublicPage(), canonicalPublicPageUuid(), shellBranding()

## App\Services\Network\PortMappingService

- Kind: class
- File: app/Services/Network/PortMappingService.php
- Public methods: __construct(), openPort(), closePort()

## App\Services\Network\SiteProvisioningService

- Kind: class
- File: app/Services/Network/SiteProvisioningService.php
- Public methods: __construct(), provisionStaticSite(), destroySite()

## App\Services\Network\TraefikLabelBuilder

- Kind: class
- File: app/Services/Network/TraefikLabelBuilder.php
- Public methods: __construct(), buildSiteLabels(), buildHostRule()

## App\Services\Notifications\DiscordNotifier

- Kind: class
- File: app/Services/Notifications/DiscordNotifier.php
- Public methods: __construct(), sendWebhook(), sendBotDm()

## App\Services\Notifications\DiscordService

- Kind: class
- File: app/Services/Notifications/DiscordService.php
- Public methods: __construct(), dispatchTwoFactorChallenge()

## App\Services\Notifications\MailService

- Kind: class
- File: app/Services/Notifications/MailService.php
- Public methods: __construct(), sendMfaOtp()

## App\Services\Notifications\OperatorAlertSink

- Kind: interface
- File: app/Services/Notifications/OperatorAlertSink.php
- Public methods: isConfigured(), sendMessage()

## App\Services\Notifications\TelegramNotifier

- Kind: class
- File: app/Services/Notifications/TelegramNotifier.php
- Public methods: __construct(), isConfigured(), sendMessage(), formatIncident()

## App\Services\Notifications\TelegramService

- Kind: class
- File: app/Services/Notifications/TelegramService.php
- Public methods: __construct(), dispatchTwoFactorChallenge(), registerVerifiedCallback(), authorizeCallback()

## App\Services\Platform\BackupService

- Kind: class
- File: app/Services/Platform/BackupService.php
- Public methods: __construct(), requestCreateSite(), requestCreateDb(), requestRunPlan(), handleCreate(), handleRunPlan()

## App\Services\Platform\IncidentService

- Kind: class
- File: app/Services/Platform/IncidentService.php
- Public methods: __construct(), openServerDown(), resolveServerRecovered(), openSchedulerFailure(), openWorkerDegraded(), resolveWorkerRecovered()

## App\Services\Platform\MonitoringService

- Kind: class
- File: app/Services/Platform/MonitoringService.php
- Public methods: __construct(), ingestMetrics(), ingestLogs(), emitServerDown(), emitServerRecovered()

## App\Services\Platform\OperationsService

- Kind: class
- File: app/Services/Platform/OperationsService.php
- Public methods: __construct(), requestNginxReload(), requestPhpRestart(), requestPhpReload(), requestSslRenew(), requestDatabaseExport(), handleNginxReload(), handlePhpRestart(), handlePhpReload(), handleSslRenew(), handleDatabaseExport()

## App\Services\Plugins\PluginInterface

- Kind: interface
- File: app/Services/Plugins/PluginInterface.php
- Public methods: getName(), getVersion(), register(), boot()

## App\Services\Plugins\PluginManagerService

- Kind: class
- File: app/Services/Plugins/PluginManagerService.php
- Public methods: __construct(), discover(), registerAll(), bootAll(), getProviders()

## App\Services\Plugins\ServiceProvider

- Kind: class
- File: app/Services/Plugins/ServiceProvider.php
- Public methods: register(), boot(), install(), uninstall()

## App\Services\Runtime\AllocationPoolService

- Kind: class
- File: app/Services/Runtime/AllocationPoolService.php
- Public methods: __construct(), allocateForInstance()

## App\Services\Runtime\ContainerService

- Kind: class
- File: app/Services/Runtime/ContainerService.php
- Public methods: __construct(), listContainers(), inspect(), stats(), queueStart(), queueStop(), queueRestart(), queueKill(), startNow(), stopNow(), restartNow(), killNow()

## App\Services\Runtime\Contracts\ContainerDriverInterface

- Kind: interface
- File: app/Services/Runtime/Contracts/ContainerDriverInterface.php
- Public methods: ping(), version(), info(), listContainers(), inspectContainer(), startContainer(), stopContainer(), restartContainer(), killContainer(), containerStats(), createContainer(), removeContainer()

## App\Services\Runtime\Drivers\AgentRuntimeDriver

- Kind: class
- File: app/Services/Runtime/Drivers/AgentRuntimeDriver.php
- Public methods: __construct(), ping(), version(), info(), listContainers(), inspectContainer(), startContainer(), stopContainer(), restartContainer(), killContainer(), containerStats(), createContainer(), removeContainer()

## App\Services\Runtime\FileGatewaysService

- Kind: class
- File: app/Services/Runtime/FileGatewaysService.php
- Public methods: __construct(), list(), options(), save(), fixPermissions()

## App\Services\Runtime\InstanceActivityService

- Kind: class
- File: app/Services/Runtime/InstanceActivityService.php
- Public methods: __construct(), log(), getForInstance(), countForInstance()

## App\Services\Runtime\InstanceAdoptionService

- Kind: class
- File: app/Services/Runtime/InstanceAdoptionService.php
- Public methods: __construct(), adopt()

## App\Services\Runtime\InstanceDatabaseService

- Kind: class
- File: app/Services/Runtime/InstanceDatabaseService.php
- Public methods: __construct(), listForInstance(), createForInstance(), deleteForInstance(), resetPassword()

## App\Services\Runtime\InstanceDeletionService

- Kind: class
- File: app/Services/Runtime/InstanceDeletionService.php
- Public methods: __construct(), delete()

## App\Services\Runtime\InstanceJobService

- Kind: class
- File: app/Services/Runtime/InstanceJobService.php
- Public methods: __construct(), recordQueued(), listForInstance(), latestForInstances(), handleAgentAck()

## App\Services\Runtime\InstanceLogArchiverService

- Kind: class
- File: app/Services/Runtime/InstanceLogArchiverService.php
- Public methods: __construct(), tick()

## App\Services\Runtime\InstanceMutationService

- Kind: class
- File: app/Services/Runtime/InstanceMutationService.php
- Public methods: __construct(), create(), update(), transition(), delete()

## App\Services\Runtime\InstanceOwnershipPolicyService

- Kind: class
- File: app/Services/Runtime/InstanceOwnershipPolicyService.php
- Public methods: __construct(), resolveActor(), resolveAcl(), applyOwnerOnCreate(), sanitizeUpdatePayload(), authorizeInstancePermission(), authorizeContainerPermission(), allowsPermissionForRow(), allowsPermissionForIdentity()

## App\Services\Runtime\InstanceProfileService

- Kind: class
- File: app/Services/Runtime/InstanceProfileService.php
- Public methods: __construct(), getProfile(), details(), saveResources(), savePorts(), saveSteam(), saveDependencies(), cleanupBeforeDelete()

## App\Services\Runtime\InstanceQueryService

- Kind: class
- File: app/Services/Runtime/InstanceQueryService.php
- Public methods: __construct(), list(), listWithTotal(), findByNid(), findByContainerId(), connection()

## App\Services\Runtime\InstanceRecordMapperService

- Kind: class
- File: app/Services/Runtime/InstanceRecordMapperService.php
- Public methods: extractPrimaryPort(), normalizeLabels(), encodeJson(), hydrate()

## App\Services\Runtime\InstanceReinstallService

- Kind: class
- File: app/Services/Runtime/InstanceReinstallService.php
- Public methods: __construct(), requestReinstall(), clearReinstallFlag()

## App\Services\Runtime\InstanceResourcePolicyInterface

- Kind: interface
- File: app/Services/Runtime/InstanceResourcePolicyInterface.php
- Public methods: assertCanCreateBackup(), assertCanCreateDatabase(), assertCanCreateAllocation()

## App\Services\Runtime\InstanceResourcePolicyService

- Kind: class
- File: app/Services/Runtime/InstanceResourcePolicyService.php
- Public methods: __construct(), recommendCpuPct(), assertCanCreateBackup(), assertCanCreateDatabase(), assertCanCreateAllocation()

## App\Services\Runtime\InstanceScheduleService

- Kind: class
- File: app/Services/Runtime/InstanceScheduleService.php
- Public methods: __construct(), listForInstance(), create(), update(), delete(), execute()

## App\Services\Runtime\InstanceSchemaService

- Kind: class
- File: app/Services/Runtime/InstanceSchemaService.php
- Public methods: __construct(), hasColumn(), idColumn(), columns()

## App\Services\Runtime\InstanceService

- Kind: class
- File: app/Services/Runtime/InstanceService.php
- Public methods: __construct(), discover(), power(), stats(), stream()

## App\Services\Runtime\InstanceSubuserService

- Kind: class
- File: app/Services/Runtime/InstanceSubuserService.php
- Public methods: __construct(), listForInstance(), grant(), revoke(), checkPermission(), instancesForUser()

## App\Services\Runtime\InstanceTransferService

- Kind: class
- File: app/Services/Runtime/InstanceTransferService.php
- Public methods: __construct(), initiate(), cancel(), listForInstance()

## App\Services\Runtime\InstancesService

- Kind: class
- File: app/Services/Runtime/InstancesService.php
- Public methods: __construct(), create(), list(), listWithTotal(), findByNid(), findByContainerId(), update(), transition(), suspend(), unsuspend(), delete(), recommendCpuPct(), connection()

## App\Services\Runtime\LocalVfsAdapter

- Kind: class
- File: app/Services/Runtime/LocalVfsAdapter.php
- Public methods: __construct(), setRequestAllowedRoots(), list(), stat(), read(), resolveDownloadPath(), write(), delete(), move(), copy(), mkdir(), chmod(), compress(), extract(), uploadInit(), uploadChunk(), uploadFinalize()

## App\Services\Runtime\MountService

- Kind: class
- File: app/Services/Runtime/MountService.php
- Public methods: __construct(), listAll(), create(), update(), delete(), forInstance()

## App\Services\Runtime\NetworkChannelAllocationService

- Kind: class
- File: app/Services/Runtime/NetworkChannelAllocationService.php
- Public methods: __construct(), allocateForInstance()

## App\Services\Runtime\NetworkChannelMutationService

- Kind: class
- File: app/Services/Runtime/NetworkChannelMutationService.php
- Public methods: __construct(), create(), createBatch(), assign(), unbind(), update(), delete(), bulkRelease(), swap()

## App\Services\Runtime\NetworkChannelPolicyService

- Kind: class
- File: app/Services/Runtime/NetworkChannelPolicyService.php
- Public methods: channelMatchesInstance(), isEligibleForTarget(), normalizeNodeAgentId(), normalizeIp(), normalizePort(), normalizeProtocol(), normalizeRole(), normalizeScope(), extractIps(), extractPorts()

## App\Services\Runtime\NetworkChannelQueryService

- Kind: class
- File: app/Services/Runtime/NetworkChannelQueryService.php
- Public methods: __construct(), list(), nodeSummary(), findById(), findByIdentity(), findAssignedByRole()

## App\Services\Runtime\NetworkChannelsService

- Kind: class
- File: app/Services/Runtime/NetworkChannelsService.php
- Public methods: __construct(), list(), create(), createBatch(), assign(), unbind(), update(), delete(), bulkRelease(), swap(), nodeSummary(), allocateForInstance()

## App\Services\Runtime\NodeResourceLedgerService

- Kind: class
- File: app/Services/Runtime/NodeResourceLedgerService.php
- Public methods: __construct(), assertCanReserve(), snapshot()

## App\Services\Runtime\ProcessService

- Kind: class
- File: app/Services/Runtime/ProcessService.php
- Public methods: __construct(), queueRun()

## App\Services\Runtime\ProvisioningPayloadBuilderService

- Kind: class
- File: app/Services/Runtime/ProvisioningPayloadBuilderService.php
- Public methods: __construct(), buildPayload(), buildInstallPayload()

## App\Services\Runtime\ProvisioningService

- Kind: class
- File: app/Services/Runtime/ProvisioningService.php
- Public methods: __construct(), provision(), preview(), loadMatrixForProvisioning(), loadMatrixOrSnapshot()

## App\Services\Runtime\RegistryService

- Kind: class
- File: app/Services/Runtime/RegistryService.php
- Public methods: __construct(), report(), dispatch(), list(), latest(), prune()

## App\Services\Runtime\SchedulerExecutionStoreService

- Kind: class
- File: app/Services/Runtime/SchedulerExecutionStoreService.php
- Public methods: __construct(), createExecutionRecord(), attachExecutionCommandId(), updateTaskStatus(), updateTaskLastRun(), markExecutionQueuedAgain(), findExecutionIdByCommand(), findTaskIdByExecution(), normalizeExecutionResult()

## App\Services\Runtime\SchedulerScheduleService

- Kind: class
- File: app/Services/Runtime/SchedulerScheduleService.php
- Public methods: normalizeSchedule(), previewSchedule(), computeNextRunFromSemantic()

## App\Services\Runtime\SchedulerScriptHubService

- Kind: class
- File: app/Services/Runtime/SchedulerScriptHubService.php
- Public methods: __construct(), listSystemScripts(), fetchSystemScriptContent()

## App\Services\Runtime\SchedulerService

- Kind: class
- File: app/Services/Runtime/SchedulerService.php
- Public methods: __construct(), listTaskTypes(), listTasks(), getTask(), createTask(), updateTask(), deleteTask(), previewSchedule(), runTaskNow(), runDueTasks(), listExecutions(), listScriptHub(), listUserScripts(), saveUserScript(), deleteUserScript(), getUserScript(), readScript(), handleAgentAck(), queueRun()

## App\Services\Runtime\Servers\ServerCfgSyncService

- Kind: class
- File: app/Services/Runtime/Servers/ServerCfgSyncService.php
- Public methods: __construct(), read(), write(), restore()

## App\Services\Runtime\Servers\ServerLifecycleService

- Kind: class
- File: app/Services/Runtime/Servers/ServerLifecycleService.php
- Public methods: __construct(), rebuild(), reinstall(), suspend(), resume(), delete()

## App\Services\Runtime\SteamTokenManager

- Kind: class
- File: app/Services/Runtime/SteamTokenManager.php
- Public methods: remember(), get(), forget()

## App\Services\Runtime\SteamWebApiService

- Kind: class
- File: app/Services/Runtime/SteamWebApiService.php
- Public methods: __construct(), isConfigured(), getApiKey(), createGameServerAccount(), queryLoginToken(), deleteGameServerAccount(), deleteGameServerAccountByToken(), getAccountList(), resetLoginToken(), setMemo(), validateLoginToken(), queryWorkshopCollections()

## App\Services\Runtime\SudoVfsIO

- Kind: class
- File: app/Services/Runtime/SudoVfsIO.php
- Public methods: __construct(), setRequestAllowedRoots(), available(), read(), write(), delete(), mkdir(), chmod(), move(), copy(), stat(), list()

## App\Services\Runtime\VfsAuditService

- Kind: class
- File: app/Services/Runtime/VfsAuditService.php
- Public methods: __construct(), requested(), finished()

## App\Services\Runtime\VfsService

- Kind: class
- File: app/Services/Runtime/VfsService.php
- Public methods: __construct(), withActor(), setAccessContext(), list(), stat(), read(), localDownloadPath(), write(), delete(), move(), copy(), mkdir(), chmod(), compress(), extract(), uploadInit(), uploadChunk(), uploadFinalize()

## App\Services\Scheduler\CronManager

- Kind: class
- File: app/Services/Scheduler/CronManager.php
- Public methods: __construct(), listJobs(), addJob(), updateJob(), removeJob(), validateSchedule()

## App\Services\Security\Bip39Service

- Kind: class
- File: app/Services/Security/Bip39Service.php
- Public methods: __construct(), generate(), validate()

## App\Services\Security\BlindIndexService

- Kind: class
- File: app/Services/Security/BlindIndexService.php
- Public methods: __construct(), index()

## App\Services\Security\BruteForceProtector

- Kind: class
- File: app/Services/Security/BruteForceProtector.php
- Public methods: __construct(), withFail2Ban(), record(), check(), unblock(), reset(), stats()

## App\Services\Security\CloudflareKmsDeployerService

- Kind: class
- File: app/Services/Security/CloudflareKmsDeployerService.php
- Public methods: __construct(), deploy()

## App\Services\Security\Encrypter

- Kind: class
- File: app/Services/Security/Encrypter.php
- Public methods: __construct(), encrypt(), decrypt(), generateKey()

## App\Services\Security\EnvelopeEncryptionService

- Kind: class
- File: app/Services/Security/EnvelopeEncryptionService.php
- Public methods: __construct(), encryptPayload(), decryptPayload(), encrypt(), decrypt(), ensureDek(), dekFingerprint(), status()

## App\Services\Security\Fail2BanManager

- Kind: class
- File: app/Services/Security/Fail2BanManager.php
- Public methods: __construct(), listJails(), jailStatus(), unban()

## App\Services\Security\FirewallManager

- Kind: class
- File: app/Services/Security/FirewallManager.php
- Public methods: __construct(), status(), addRule(), removeRule(), enable(), disable()

## App\Services\Security\IntegrationSecretService

- Kind: class
- File: app/Services/Security/IntegrationSecretService.php
- Public methods: __construct(), set(), get(), has(), delete()

## App\Services\Security\MasterKeyManagerFactory

- Kind: class
- File: app/Services/Security/MasterKeyManagerFactory.php
- Public methods: __construct(), backendId(), backend(), ensureInitialized(), ensureRuntimeKeyAvailable(), activeMasterKeyHex(), storeMasterKeyHex(), hasMaterial(), health()

## App\Services\Security\MasterKey\AppArmorProfileService

- Kind: class
- File: app/Services/Security/MasterKey/AppArmorProfileService.php
- Public methods: ensureProfile()

## App\Services\Security\MasterKey\CloudflareZeroDiskKmsMasterKeyBackend

- Kind: class
- File: app/Services/Security/MasterKey/CloudflareZeroDiskKmsMasterKeyBackend.php
- Public methods: __construct(), id(), initialize(), hasMaterial(), ensureRuntimeKeyAvailable(), activeMasterKeyHex(), storeMasterKeyHex(), health()

## App\Services\Security\MasterKey\HardwareFingerprintService

- Kind: class
- File: app/Services/Security/MasterKey/HardwareFingerprintService.php
- Public methods: __construct(), fingerprint(), machineId(), primaryMacAddress()

## App\Services\Security\MasterKey\HybridAutoUnsealMasterKeyBackend

- Kind: class
- File: app/Services/Security/MasterKey/HybridAutoUnsealMasterKeyBackend.php
- Public methods: __construct(), id(), initialize(), hasMaterial(), ensureRuntimeKeyAvailable(), activeMasterKeyHex(), storeMasterKeyHex(), health()

## App\Services\Security\MasterKey\MasterKeyBackendInterface

- Kind: interface
- File: app/Services/Security/MasterKey/MasterKeyBackendInterface.php
- Public methods: id(), initialize(), hasMaterial(), ensureRuntimeKeyAvailable(), activeMasterKeyHex(), storeMasterKeyHex(), health()

## App\Services\Security\MasterKey\ProcessMemoryGuardService

- Kind: class
- File: app/Services/Security/MasterKey/ProcessMemoryGuardService.php
- Public methods: disableCoreDumps(), memzero()

## App\Services\Security\MasterKey\Tpm2SealedMasterKeyBackend

- Kind: class
- File: app/Services/Security/MasterKey/Tpm2SealedMasterKeyBackend.php
- Public methods: __construct(), id(), initialize(), hasMaterial(), ensureRuntimeKeyAvailable(), activeMasterKeyHex(), storeMasterKeyHex(), health()

## App\Services\Security\PermissionGuard

- Kind: class
- File: app/Services/Security/PermissionGuard.php
- Public methods: __construct(), audit(), fix(), enforce(), checkPath()

## App\Services\Security\SecretsManagerService

- Kind: class
- File: app/Services/Security/SecretsManagerService.php
- Public methods: __construct(), verifyEnvironmentIntegrity(), encryptAtRest(), decryptAtRest(), encrypt(), decrypt(), generateMasterKey(), generateMasterKeyMaterial(), triggerSelfDestruct(), isEmergencyMode(), clearEmergencyModeMarker(), getEmergencyDetails(), generateProtectedBackup(), encodeProtectedBackupForFile(), recoverFromBackup(), generateRecoveryKey(), recoverMasterKey(), keyFingerprint(), masterKeyPath(), hasMasterKey(), pendingMasterKeyPath(), hasStagedMasterKey(), readStagedMasterKey(), stagedKeyFingerprint(), initializeMasterKey(), stageMasterKey(), activateStagedMasterKey(), cleanupStagedMasterKey(), rotateEncryptedValues()

## App\Services\Security\SecretsRotationService

- Kind: class
- File: app/Services/Security/SecretsRotationService.php
- Public methods: __construct(), rotateSettingsSecrets(), rotateSettingsSecretsFromStaged(), snapshot()

## App\Services\Security\SecurityEntranceService

- Kind: class
- File: app/Services/Security/SecurityEntranceService.php
- Public methods: __construct(), current(), prefixPath(), guard(), save()

## App\Services\Security\SecurityRuntimeService

- Kind: class
- File: app/Services/Security/SecurityRuntimeService.php
- Public methods: __construct(), firewallStatus(), firewallAdd(), firewallRemove(), firewallEnable(), firewallDisable(), fail2BanJails(), fail2BanStatus(), fail2BanUnban(), sshConfig()

## App\Services\Security\SshManager

- Kind: class
- File: app/Services/Security/SshManager.php
- Public methods: __construct(), config()

## App\Services\Security\SudoGuard

- Kind: class
- File: app/Services/Security/SudoGuard.php
- Public methods: __construct(), isProtected(), grant(), verify(), requireFor(), revoke()

## App\Services\Security\TwoFactorGate

- Kind: class
- File: app/Services/Security/TwoFactorGate.php
- Public methods: __construct(), issue(), status(), registerCallback(), consume(), revoke()

## App\Services\Settings\SettingsService

- Kind: class
- File: app/Services/Settings/SettingsService.php
- Public methods: __construct(), listAll(), categories(), reveal(), set(), getString(), get(), exportSettings(), importSettings(), exportAll(), previewImportAll(), importAll(), delete()

## App\Services\Setup\SetupFoundationSchemaService

- Kind: class
- File: app/Services/Setup/SetupFoundationSchemaService.php
- Public methods: __construct(), report(), ensure()

## App\Services\Setup\SetupInstallRunEventPersistenceService

- Kind: class
- File: app/Services/Setup/SetupInstallRunEventPersistenceService.php
- Public methods: __construct(), append(), list()

## App\Services\Setup\SetupInstallRunPersistenceService

- Kind: class
- File: app/Services/Setup/SetupInstallRunPersistenceService.php
- Public methods: __construct(), upsertFromState()

## App\Services\Setup\SetupIntegrationsService

- Kind: class
- File: app/Services/Setup/SetupIntegrationsService.php
- Public methods: __construct(), templates(), save(), verify()

## App\Services\Setup\SetupRestoreService

- Kind: class
- File: app/Services/Setup/SetupRestoreService.php
- Public methods: __construct(), acknowledgeRekeyDownload(), prepare(), report(), apply()

## App\Services\Setup\SetupSecurityService

- Kind: class
- File: app/Services/Setup/SetupSecurityService.php
- Public methods: __construct(), initialize(), inventory()

## App\Services\Setup\SetupStateService

- Kind: class
- File: app/Services/Setup/SetupStateService.php
- Public methods: __construct(), status(), isInstalled(), start(), saveProfile(), saveSecurity(), saveIntegrations(), saveRestore(), complete(), events()

## App\Services\Sso\JwtService

- Kind: class
- File: app/Services/Sso/JwtService.php
- Public methods: __construct(), encode(), decode()

## App\Services\Sso\OAuthClientService

- Kind: class
- File: app/Services/Sso/OAuthClientService.php
- Public methods: __construct(), createClient(), rotateSecret(), getClient(), listClients(), updateClient(), deleteClient(), verifySecret(), validateRedirectUri()

## App\Services\Sso\OidcKeyManager

- Kind: class
- File: app/Services/Sso/OidcKeyManager.php
- Public methods: __construct(), getKid(), getPublicKeyPem(), getJwks(), sign(), verify()

## App\Services\Sso\OidcServerService

- Kind: class
- File: app/Services/Sso/OidcServerService.php
- Public methods: __construct(), createAuthorizationCode(), exchangeCode(), refreshToken(), clientCredentials(), revokeToken(), getUserInfo(), hasConsent(), grantConsent(), resolveUser()

## App\Services\Sso\SequenceGeneratorService

- Kind: class
- File: app/Services/Sso/SequenceGeneratorService.php
- Public methods: __construct(), next(), register(), updateSequenceSettings(), getSequence()

## App\Services\System\HostMonitor

- Kind: class
- File: app/Services/System/HostMonitor.php
- Public methods: __construct(), getSnapshot(), getHostInfo(), getCpuUsage(), getMemoryInfo(), getDiskInfo(), getNetworkInfo(), getNetworkRate(), getDiskIoRate(), getLoadAverage(), getUptime(), getTopProcesses(), dropCaches(), pruneDocker()

## App\Services\System\NginxTempHealthService

- Kind: class
- File: app/Services/System/NginxTempHealthService.php
- Public methods: __construct(), check(), checkAndAlert()

## App\Services\Terminal\LogViewerService

- Kind: class
- File: app/Services/Terminal/LogViewerService.php
- Public methods: __construct(), listFiles(), tail(), since()

## App\Services\Websites\NginxManager

- Kind: class
- File: app/Services/Websites/NginxManager.php
- Public methods: __construct(), listSites(), getSiteConfig(), saveSiteConfig(), setSitePhpTarget(), enableSslForSite(), createSite(), adoptSite(), revertSiteConfig(), testConfig(), reload(), getRewriteRules(), saveRewriteRules(), deleteSite()

## App\Services\Websites\PhpFpmManager

- Kind: class
- File: app/Services/Websites/PhpFpmManager.php
- Public methods: __construct(), versions(), snapshot(), restart(), reload(), normalizeVersion(), socketForVersion(), iniPath(), binaryPath(), modules(), detectSiteVersion()

## App\Services\Websites\PhpIniService

- Kind: class
- File: app/Services/Websites/PhpIniService.php
- Public methods: __construct(), snapshot(), save()

## App\Services\Websites\SslManager

- Kind: class
- File: app/Services/Websites/SslManager.php
- Public methods: __construct(), listCertificates(), getCertificateInfo(), checkExpiry(), scanExpiring(), renewCertificate(), issueCertificate()

## App\Services\Websites\SudoIO

- Kind: class
- File: app/Services/Websites/SudoIO.php
- Public methods: __construct(), read(), write(), exists(), stat(), listFiles(), listDirs(), copy(), symlink(), delete(), deleteTree()

## App\Services\Websites\WebsiteRuntimeService

- Kind: class
- File: app/Services/Websites/WebsiteRuntimeService.php
- Public methods: __construct(), sites(), siteConfig(), createSite(), adoptSite(), saveSiteConfig(), setSitePhpVersion(), revertSiteConfig(), deleteSite(), rewriteRules(), saveRewriteRules(), nginxTest(), nginxReload(), phpRestart(), phpReload(), phpSnapshot(), sslCertificates(), sslCertificateInfo(), sslExpiring(), sslRenew(), sslIssue()
