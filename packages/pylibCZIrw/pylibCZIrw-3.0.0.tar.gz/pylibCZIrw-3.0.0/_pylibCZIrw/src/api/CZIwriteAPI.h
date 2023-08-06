#pragma once

#include "inc_libCzi.h"
#include "PImage.h"
#include <iostream>
#include <optional>

/// Class used to represent a CZI writer object in pylibCZIrw. 
/// It gathers the libCZI features for writing needed in the pylibCZI project.
/// CZIrwAPI will be exposed to python via pybind11 as a czi class.
class CZIwriteAPI
{

private:

	std::shared_ptr <libCZI::ICziWriter>	spWriter;	///< The pointer to the spWriter.

public:

	/// Constructor which constructs a CZIwriteAPI object from the given wstring.
	/// Creates a spWriter for the czi document pointed by the given filepath.
	CZIwriteAPI(const std::wstring& fileName);

	/// Close the Opened czi writer.
	void close() { this->spWriter->Close(); }

	void WriteMetadata(const std::wstring& documentTitle, std::optional<double> scaleX, std::optional<double> scaleY, std::optional<double> scaleZ, const std::map<int, std::string>& channelNames);

	/// Add the specified bitmap subblock to the czi document
	static void AddSubBlock(const libCZI::CDimCoordinate& coord,const PImage* subblock,libCZI::ICziWriter* writer, int x, int y, int m);

	/// Add the specified bitmap plane to the czi document at the specified coordinates.
	bool AddTile(const std::string& coordinateString,const PImage* plane, int x, int y, int m);

};