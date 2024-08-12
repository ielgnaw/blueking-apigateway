interface IAuthConfig {
  auth_verified_required: boolean;
  app_verified_required: boolean;
  resource_perm_required: boolean;
}

interface IBackendConfig {
  method: string;
  path: string;
  match_subpath: boolean;
  timeout: number;
}

interface IBackend {
  name: string;
  config: IBackendConfig;
}

interface IImportedResource {
  id?: number | null;
  name: string;
  description?: string | null;
  description_en?: string | null;
  method: string;
  path: string;
  match_subpath: boolean;
  is_public: boolean;
  allow_apply_permission: boolean;
  doc: any[] | null;
  auth_config?: IAuthConfig;
  backend: IBackend;
  labels: any[] | null;
  openapi_schema: Record<string, any>;
  plugin_configs?: any | null;
}

export { IBackend, IBackendConfig, IAuthConfig, IImportedResource };
