# natural-language-processing_tweet
tweet情報を元に2-gramと形態素解析からのgram判定を行うスクリプト

#スクリプト簡易説明
**sqlite_twitter**...db、table作成。tableへのinsertを担当する。
**sqlite_select**...table内のアクセス。コメントをselectする。
**streaming_location**...日本国内のtweetを収集(streaming)。
**streaming_tweet**...日本語判定されているtweetを収集(同上)。
**n-gram**...2-gramと形態素解析での実装。
