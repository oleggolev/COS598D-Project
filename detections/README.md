# Using the PIFSC HARP Dataset

## Audio

Each audio file is a FLAC-compressed XWAV file. XWAV files are WAV files, but
they have a custom data subchunk with file-level metadata and a list of start
times and offsets of sections of the file called "subchunks." In most of this
archive, each subchunk is 75 seconds long, but there is a duty cycle which
leaves some unrecorded time between subchunks.

The FLAC command should be used with the --keep-foreign-metadata flag to
preserve the XWAV custom data subchunk, for which the binary format is.


*flac -df --delete-input-file --preserve-modtime --keep-foreign-metadata <path to file>*


**Raw Data Citation**

NOAA Pacific Islands Fisheries Science Center. 2021. *Pacific Islands Passive Acoustic Network (PIPAN) 10kHz Data.*
NOAA National Centers for Environmental Information. [https://doi.org/10.25921/Z787-9Y54](https://doi.org/10.25921/Z787-9Y54) access date

## CSV

The annotations.csv file lists time intervals where various sound types are
present. These intervals were identified in several rounds of effort by human
annotators. Detailed descriptions of the sampling strategies and motivation for
each effort can be found in

A. Allen et al., ["A convolutional neural network for automated detection of
humpback whale song in a diverse, long-term passive acoustic
dataset"](https://www.frontiersin.org/articles/10.3389/fmars.2021.607321),
*Front. Mar. Sci.*, 2021, doi: 10.3389/fmars.2021.607321.

See especially "Table 1."

The majority of the annotations indicate the presence of humpback whale
(Megaptera novaeangliae), but some identify other sound types that detectors may
confuse with humpback whale.

### Erratum
As of 2022-07-27, the current annotations.csv replaces an earlier version, with
the same name, in the UTC label endpoings of many rows were 8 hours too early.

## CSV Format

### Columns

*   *audit_name* (enum) identifies which of the efforts was the source of the
    annotation in that row.
*   *flac_compressed_xwav_object* (string) a fully-qualified Google Cloud
    Storage path to a FLAC file within which the annotation was made. Include
    the --keep-foreign-metadata flag when uncompressing.
*   *subchunk_index* (integer) identifies the 75-second subchunk within which
    the annotation was made as a 0-based index into the list of subchunks in the
    XWAV header.
*   *label_is_strong* (boolean) indicates whether the time bounds are tight,
    meaning the vocalization occupies the entire interval. Where this field is
    false, the annotation is a subchunk-level label, meaning the sound event is
    present somewhere in the subchunk but not necessarily continuously.
*   *implicit_negatives* (boolean) whether unlabeled time intervals in the
    subchunk identified in the current row were audited and definitely did
    **not** contain sounds with the same label in the row. This is false for
    audit efforts that reviewed batches of few-second intervals out of context
    from the subchunks from which they had been extracted. (This is relevant,
    for instance, if assuming that unannotated regions in this subchunk make
    good negative training examples for a learned detector.)
*   *label* (enum) code for the sound event type annotated in this row; the
    species code when it is an animal; the list of possible codes is below.
*   *begin_rel_subchunk* (float) offset in seconds from the beginning of the
    subchunk to the beginning of the time interval annotated in this row.
*   *end_rel_subchunk* (float) offset in seconds from the beginning of the
    subchunk to the end of the time interval annotated in this row.
*   *begin_utc* (string; ISO-8601 datetime) UTC time of the beginning of the
    time interval annotated in this row.
*   *end_utc* (string; ISO-8601 datetime) UTC time of the end of the time
    interval annotated in this row.

## Label Vocabulary

Label        | Description
------------ | --------------------------------------
Background   | Environmental sounds only
Device       | Noise from the recording equipment
Fish         | Fish sound not otherwise identified
Mn           | Humpback whale
Other        | None of the other sound types
Vessel       | Vessel noise
