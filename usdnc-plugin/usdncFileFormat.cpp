#include "usdncFileFormat.h"
#include "pxr/base/tf/registryManager.h"
#include "pxr/base/tf/type.h"
#include "pxr/usd/sdf/layer.h"
#include "pxr/usd/sdf/abstractData.h"

PXR_NAMESPACE_OPEN_SCOPE

TF_DEFINE_PUBLIC_TOKENS(UsdncFileFormatTokens, UsdncFileFormatTokens);

TF_REGISTRY_FUNCTION(TfType) {
    TfType::Define<UsdncFileFormat, TfType::Bases<SdfFileFormat>>();
}

extern "C" {
    SdfFileFormat* UsdncFileFormat_FactoryCreate() {
        return new UsdncFileFormat();
    }
}

UsdncFileFormat::UsdncFileFormat() 
    : SdfFileFormat(UsdncFileFormatTokens->Id, 
                    UsdncFileFormatTokens->Version, 
                    UsdncFileFormatTokens->Target, 
                    UsdncFileFormatTokens->Id) {}

UsdncFileFormat::~UsdncFileFormat() {}

bool UsdncFileFormat::CanRead(const std::string& filePath) const {
    return true; 
}

bool UsdncFileFormat::Read(SdfLayer* layer, const std::string& resolvedPath, bool metadataOnly) const {
    if (!layer) return false;

    SdfFileFormatConstPtr usdcFormat = SdfFileFormat::FindById(TfToken("usdc"));
    if (usdcFormat) {
        SdfLayerRefPtr tmpLayer = SdfLayer::CreateAnonymous(".usdc");
        if (usdcFormat->Read(get_pointer(tmpLayer), resolvedPath, metadataOnly)) {
            layer->TransferContent(tmpLayer); 
            return true;
        }
    }
    
    SdfFileFormatConstPtr usdaFormat = SdfFileFormat::FindById(TfToken("usda"));
    if (usdaFormat) {
        SdfLayerRefPtr tmpLayer = SdfLayer::CreateAnonymous(".usda");
        if (usdaFormat->Read(get_pointer(tmpLayer), resolvedPath, metadataOnly)) {
            layer->TransferContent(tmpLayer);
            return true;
        }
    }

    return false;
}

bool UsdncFileFormat::WriteToFile(const SdfLayer& layer, const std::string& filePath, const std::string& comment, const FileFormatArguments& args) const {
    SdfFileFormatConstPtr usdcFormat = SdfFileFormat::FindById(TfToken("usdc"));
    return usdcFormat && usdcFormat->WriteToFile(layer, filePath, comment, args);
}

PXR_NAMESPACE_CLOSE_SCOPE

