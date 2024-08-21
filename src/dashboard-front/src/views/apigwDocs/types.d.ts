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

export {
  TabType,
  // SdkType,
  IGateway,
  ISdk,
  IResourceVersion,
  ISdkObject,
};
