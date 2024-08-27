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
  name: string;
  description: string;
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
};
