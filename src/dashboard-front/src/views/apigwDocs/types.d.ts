type TabType = 'apigw' | 'component';
// type SdkType = 'apigateway' | 'esb';

interface IGateway {
  id: number;
  name: string;
  description: string;
}

interface ISdk {
  language: string;
  version: string;
  url: string;
  name: string;
  install_command: string;
}

interface IResourceVersion {
  id: number;
  version: string;
}

interface ISdkObject {
  gateway: IGateway;
  sdk: ISdk;
  resource_version: IResourceVersion;
  released_stages: any[];
}

interface ISystem {
  board: string;
  board_label: string;
  categories: ICategory[];
}

interface ICategory {
  id: string;
  name: string;
  systems: IComponent[];
  _navId?: string;
}

interface IComponent {
  id: number;
  name: string;
  description: string;
  verified_app_required: boolean;
  verified_user_required: boolean;
  component_permission_required: boolean;
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

interface IApiGatewayBasics {
  id: number;
  name: string;
  description: string;
  maintainers: string[];
  is_official: boolean;
  api_url: string;
}


interface IComponentBasics {
  name: string;
  description: string;
  comment: string;
  maintainers: string[];
}

export {
  TabType,
  // SdkType,
  IGateway,
  ISdk,
  IResourceVersion,
  ISdkObject,
  ISystem,
  ICategory,
  IComponent,
  IResource,
  IApiGatewayBasics,
  IComponentBasics,
};
