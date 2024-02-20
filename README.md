# YouTube Data Aggregator

This versatile script allows users to gather valuable information from channels on YouTube efficiently. By providing unique identifiers, names, subscription counts, bios, and details of recently published video collections, the tool simplifies analyzing various channels effortlessly. Furthermore, it supports batch processing for simultaneous analysis of numerous channels.

## Features

- Retrieve essential metadata including unique ID, name, subscriber count, profile description, and recent 50 uploaded videos.
- Process several channels together seamlessly.
- Obtain rich insights such as titles, views, likes, dislikes, number of comments, associated comments, and individuals leaving remarks.

## Usage Example

Suppose you wanted to analyze popular tech reviewers Linus Tech Tips and Marques Brownlee. Simply execute the script passing their respective channel ids:

```sh
$ ./DataAggregation.py -c https://www.youtube.com/@ThinkMediaTV,https://www.youtube.com/@AutoFocus,https://www.youtube.com/@cut,https://www.youtube.com/@LofiGirl
```
