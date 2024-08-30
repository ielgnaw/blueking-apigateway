type TabType = 'apigw' | 'component';

interface ICategory {
  id: string;
  name: string;
  systems: IComponent[];
  _navId?: string;
}

interface INavItem {
  id: number | string;
  name: string;
}

type LanguageType = 'python' | 'java';

// 网关类型

interface IApiGatewayBasics {
  id: number;
  name: string;
  description: string;
  maintainers: string[];
  is_official: boolean;
  api_url: string;
}

interface IApiGatewaySdk {
  language: LanguageType;
  resource_version: IResourceVersion;
  sdk?: any;
  stage: { id: number, name: string }
}

interface IResourceVersion {
  id: number;
  version: string;
}

interface IResource {
  id: number;
  name: string;
  description: string;
  method: string;
  path: string;
  verified_user_required: boolean;
  verified_app_required: boolean;
  resource_perm_required: boolean;
  labels: string[];
}

interface IStage {
  id: number;
  name: string;
  description: string;
}

// 组件类型

interface ISystem {
  board: string;
  board_label: string;
  categories: ICategory[];
  sdk?: IComponentSdk;
}

interface ISystemBasics {
  name: string;
  description: string;
  comment: string;
  maintainers: string[];
}

interface IComponent {
  id: number;
  name: string;
  description: string;
  verified_app_required: boolean;
  verified_user_required: boolean;
  component_permission_required: boolean;
}

interface IComponentSdk {
  board_label: string;
  sdk_name: string;
  sdk_description: string;
  sdk_version_number: string;
  sdk_download_url: string;
  sdk_install_command: string;
  language: LanguageType;
}

export {
  IApiGatewayBasics,
  IApiGatewaySdk,
  ICategory,
  IComponent,
  IComponentSdk,
  INavItem,
  IResource,
  IResourceVersion,
  IStage,
  ISystem,
  ISystemBasics,
  LanguageType,
  TabType,
};
