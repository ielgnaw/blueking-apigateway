type TRequestMethod = 'ANY' | 'DELETE' | 'GET' | 'PATCH' | 'POST' | 'PUT';

interface IAuthConfig {
  auth_verified_required: boolean;
  app_verified_required: boolean;
  resource_perm_required: boolean;
}

interface IBackendConfig {
  method: TRequestMethod;
  path: string;
  match_subpath: boolean;
  timeout: number;
}

interface IBackend {
  name: string;
  config: IBackendConfig;
}

interface IImportedResource {
  allow_apply_permission: boolean;
  auth_config?: IAuthConfig;
  backend?: IBackend;
  description?: string | null;
  description_en?: string | null;
  doc: any[] | null;
  id: number | null;
  is_public: boolean;
  label_ids?: number[];
  labels: any[] | null;
  match_subpath: boolean;
  method: TRequestMethod;
  name: string;
  openapi_schema: Record<string, any>;
  path: string;
  plugin_configs?: any | null;
}

interface ILocalImportedResource extends Partial<IImportedResource> {
  _localId: number;
  _unchecked: boolean;
}

export { IBackend, IBackendConfig, IAuthConfig, IImportedResource, ILocalImportedResource };
