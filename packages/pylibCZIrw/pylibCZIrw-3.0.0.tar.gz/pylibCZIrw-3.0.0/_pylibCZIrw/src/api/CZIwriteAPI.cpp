#include "CZIwriteAPI.h"
#include <optional>

using namespace libCZI;
using namespace std;

CZIwriteAPI::CZIwriteAPI(const std::wstring& fileName) {

	auto stream = libCZI::CreateOutputStreamForFile(fileName.c_str(), true);
	auto spWriter = libCZI::CreateCZIWriter();

	// initialize the "CZI-writer-object" with the "output-stream-object"
	// notes: (1) not sure if we should/have to provide a "bounds" at initialization
	//        (2) the bounds provided here _could_ be used to create a suitable sized subblk-directory at the
	//             beginning of the file AND for checking the validity of the subblocks added later on
	//        (3) ...both things are not really necessary from a technical point of view, however... consistency-
	//             checking I'd consider an important feature

	auto spWriterInfo = make_shared<CCziWriterInfo>(GUID{ 0,0,0,{ 0,0,0,0,0,0,0,0 } });

	spWriter->Create(stream, spWriterInfo);

	this->spWriter = spWriter;
}


/*static*/void CZIwriteAPI::AddSubBlock(const libCZI::CDimCoordinate& coord,const PImage* subblock, libCZI::ICziWriter* writer, int x, int y, int m) {
	
	const void* sbBlkMetadata;
	uint32_t sbBlkMetadataSize;

	std::string sbMdXml;

	if (sbMdXml.empty())
	{
		sbBlkMetadata = nullptr;
		sbBlkMetadataSize = 0;
	}
	else
	{
		sbBlkMetadata = sbMdXml.c_str();;
		sbBlkMetadataSize = static_cast<uint32_t>(sbMdXml.size());
	}

	AddSubBlockInfoStridedBitmap addInfo;
	addInfo.Clear();

	addInfo.coordinate = coord;
	addInfo.mIndexValid = true;
	addInfo.mIndex = m;
	addInfo.x = x;
	addInfo.y = y;
	addInfo.logicalWidth = subblock->get_width();
	addInfo.logicalHeight = subblock->get_height();
	addInfo.physicalWidth = subblock->get_width();
	addInfo.physicalHeight = subblock->get_height();
	addInfo.PixelType = subblock->get_pixelType();
	addInfo.ptrBitmap = subblock->get_data();
	addInfo.strideBitmap = subblock->get_stride();
	addInfo.ptrSbBlkMetadata = sbBlkMetadata;
	addInfo.sbBlkMetadataSize = sbBlkMetadataSize;
	writer->SyncAddSubBlock(addInfo);
};


bool CZIwriteAPI::AddTile(const std::string& coordinateString,const PImage* plane, int x, int y, int m) {

	libCZI::CDimCoordinate* coords = new libCZI::CDimCoordinate();
	bool conversion_to_cdim = Utils::StringToDimCoordinate(coordinateString.c_str(), coords);
	
	this->AddSubBlock(coords, plane, this->spWriter.get(), x, y, m);

	return true;
};


void CZIwriteAPI::WriteMetadata(const std::wstring& documentTitle, const std::optional<double> scaleX, const std::optional<double> scaleY, const std::optional<double> scaleZ, const std::map<int, std::string>& channelNames) {

	// get "partially filled out" metadata - the metadata contains information which was derived from the 
	//  subblocks added, in particular we "pre-fill" the Size-information, and the Pixeltype-information
	PrepareMetadataInfo prepareInfo;
	prepareInfo.funcGenerateIdAndNameForChannel = [&channelNames](int channelIndex)->tuple<string, tuple<bool, string>>
	{
		stringstream ssId, ssName;
		ssId << "Channel:" << channelIndex;
		auto channelNameIterator = channelNames.find(channelIndex);
		bool nameIsValid;
		if (channelNameIterator != channelNames.end())
		{
			ssName << channelNameIterator->second;
			nameIsValid = true;
		}
		else
		{
			ssName << "";
			nameIsValid = false;
		}
		return make_tuple(ssId.str(), make_tuple(true, ssName.str()));
	};

	auto mdBldr = this->spWriter->GetPreparedMetadata(prepareInfo);

	// now we could add additional information
	GeneralDocumentInfo docInfo;
	docInfo.SetTitle(documentTitle);
	docInfo.SetComment(L"pylibCZIrw generated");
	MetadataUtils::WriteGeneralDocumentInfo(mdBldr.get(), docInfo);

	// Add scaleinfo
	ScalingInfo scaleInfo;
	if (scaleX.has_value())
	{
		scaleInfo.scaleX = scaleX.value();
	}
	if (scaleY.has_value())
	{
		scaleInfo.scaleY = scaleY.value();
	}
	if (scaleZ.has_value())
	{
		scaleInfo.scaleZ = scaleZ.value();
	}
	MetadataUtils::WriteScalingInfo(mdBldr.get(), scaleInfo);

	mdBldr->GetRootNode()->GetOrCreateChildNode("Metadata/Information/Application/Name")->SetValue("pylibCZIrw");
	mdBldr->GetRootNode()->GetOrCreateChildNode("Metadata/Information/Application/Version")->SetValue("3.0.0");

	// the resulting metadata-information is written to the CZI here
	auto xml = mdBldr->GetXml(true);
	WriteMetadataInfo writerMdInfo = { 0 };
	writerMdInfo.szMetadata = xml.c_str();
	writerMdInfo.szMetadataSize = xml.size();
	this->spWriter->SyncWriteMetadata(writerMdInfo);
}