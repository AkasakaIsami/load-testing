for i in {0..9}; do
    python3 create_and_start_conference.py
    python3 submit_article.py
    python3 first_review_article.py
    python3 rebuttal.py
    python3 second_review_article.py
    python3 read_message.py
done

for i in {0..49}; do
    python3 query.py
done
