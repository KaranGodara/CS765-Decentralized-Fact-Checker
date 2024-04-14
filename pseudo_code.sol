// SPDX-License-Identifier: MIT
pragma solidity >=0.6.12 <0.9.0;

contract DApp {
    // Creater of the contract
    address creator;

    // genre specific detials for trustworthiness
    struct trust_details {
        uint genre_trust;
        uint max_genre_trust;
        uint num_correct;
        uint num_incorrect;
        int net_curr_score;
        uint curr_net_required;
    }

    // Overall struct to map trust specific to each genre
    struct trust {
        mapping(bytes32 => trust_details) trust_data;
    }

    // Map to store trustworthiness of each address address for every genre of news
    mapping(address => trust) trustworthiness;

    // This mapping would store the daily average news request that would be used to calculate trust
    mapping(bytes32 => uint) daily_average_news_request;

    // This mapping would store the current daily average news request that would be used to update
    // the estimate of daily_average_news_request
    mapping(bytes32 => uint) curr_news_request;
    uint256 last_time_of_updation;

    // Map to keep the
    mapping(address => uint) public balances;

    // Storing the genres in a list
    bytes32[] public genres;

    // Storing the list of all the addresses in the DApp
    address[] voters;

    // Minium deposit required to be a voter
    // Minimum fees required to put news up for verification
    // Minimum fees required to add new genre to the list
    uint constant deposit = 1 ether;
    uint constant min_fees = 2 ether;
    uint constant fees_to_add_new_genre = 5 ether;

    // Mapping from hash of news to actual news in string
    mapping(bytes32 => string) hash_to_news;
    mapping(string => bytes32) news_to_hash;

    // Mapping from hash of news to fees paid for news verification
    mapping(bytes32 => uint) fees_for_news;

    // Store the total weight of all the voters currently active in each genre
    mapping(bytes32 => uint) total_votes;

    // Mapping to store the fakeness or reallness of any news, 1 indicates real, -1 indicates
    // false and 0 indicates no decision taken on such a news
    mapping(bytes32 => int8) is_real;

    // Time period for voting
    uint256 voting_period = 120 minutes;

    // Mapping to store the time at which a news was put into the DApp for voting and its genre
    mapping(bytes32 => uint256) news_put_time;
    mapping(bytes32 => bytes32) news_genre;
    mapping(bytes32 => address) news_sender;

    // We now store, total votes casted for a news within the stipulated time period of voting for the news
    // We only make a decision on the news if the number of total votes casted is atleast 25% of the total
    // active votes of the system
    mapping(bytes32 => uint) total_votes_casted_to_news;
    mapping(bytes32 => int) net_votes_casted_to_news;

    // We store a list of names of voters who voted for the news and what they voted
    struct vote_casted {
        bool vote;
        address voter;
    }
    mapping(bytes32 => vote_casted[]) votes_casted_to_news;

    // Constructor code is only run when the contract is created
    constructor() {
        // Here in we will first set the basic list of genres available
        genres.push("Sports");
        genres.push("Finance");
        genres.push("Science");
        genres.push("Politics");
        genres.push("Entertainment");
        genres.push("Miscellaneous");

        // Setting the total votes as 0 initially
        for (uint i = 0; i < genres.length; i++) {
            total_votes[genres[i]] = 0;
        }

        // Setting up the value for future updates
        last_time_of_updation = block.timestamp;

        // Setting the creator
        creator = msg.sender;
    }

    // Function that takes some deposit and makes the caller a voter
    function register() external payable {
        require(
            msg.value >= deposit,
            "Minimum deposit required to become voter is 1 ETH"
        );
        balances[msg.sender] += msg.value;

        // Updating the total_votes of the system, note it may be the case than voter registering
        // now had de-registered in the past and then is registering again. Hence, we add value stored
        // in trustworthiness mapping for that user, which is zero by default for new user.
        for (uint i = 0; i < genres.length; i++) {
            // For new voter, trustworthiness should start from 1 and not 0
            if (
                trustworthiness[msg.sender].trust_data[genres[i]].genre_trust <
                1
            ) {
                trustworthiness[msg.sender]
                    .trust_data[genres[i]]
                    .genre_trust = 1;
                trustworthiness[msg.sender]
                    .trust_data[genres[i]]
                    .max_genre_trust = 100;

                trustworthiness[msg.sender]
                    .trust_data[genres[i]]
                    .num_correct = 0;
                trustworthiness[msg.sender]
                    .trust_data[genres[i]]
                    .num_incorrect = 0;

                trustworthiness[msg.sender]
                    .trust_data[genres[i]]
                    .net_curr_score = 0;
                trustworthiness[msg.sender]
                    .trust_data[genres[i]]
                    .curr_net_required = 1;
            }

            total_votes[genres[i]] += trustworthiness[msg.sender]
                .trust_data[genres[i]]
                .genre_trust;
        }
    }

    // Function that voter can use to de-register and become non-voter, by doing this they get
    // all the money back stored in the contract for them that is both the depost and any money
    // they may have earned by voting
    function deregister() external payable {
        require(balances[msg.sender] >= deposit, "You are not a voter");
        uint temp = balances[msg.sender];
        balances[msg.sender] = 0;

        // Updating the total_votes of the system
        for (uint i = 0; i < genres.length; i++) {
            total_votes[genres[i]] -= trustworthiness[msg.sender]
                .trust_data[genres[i]]
                .genre_trust;
        }

        // Returning the money to the voter
        payable(msg.sender).transfer(temp);
    }

    // Function that users can call to get a list of genres available to categorise the news
    function get_genres() public view returns (bytes32[] memory) {
        return genres;
    }

    // Users or Voters can check what is the money they can withdraw from the contract
    function get_balance() external view returns (uint) {
        return balances[msg.sender];
    }

    // Function that voters can call to get extra money than the deposit from their account in the
    // contract, without being removed as voter
    function withdraw_money(uint money) external payable {
        require(
            balances[msg.sender] >= deposit + money,
            "You can't withdraw money such that deposit isn't left behind"
        );
        balances[msg.sender] -= money;
        payable(msg.sender).transfer(money);
    }

    // keccak256(), would use this to store the hash of the news (initially sent in the form of string) for voting
    // and accessing
    function upload_news_for_review(
        string calldata news,
        bytes32 genre_news
    ) public payable {
        // Firstly checking if enough fees paid or not
        require(
            msg.value >= min_fees,
            "Must pay atleast minimum fees of 2 ETH to start verification of a news"
        );

        // Convert string to bytes
        bytes memory newsBytes = bytes(news);

        // Compute hash of the string
        bytes32 newsHash = keccak256(newsBytes);

        // Store news content in hash mapping
        hash_to_news[newsHash] = news;
        news_to_hash[news] = newsHash;

        // Marking the time at which the news came into the DApp
        news_put_time[newsHash] = block.timestamp;
        news_genre[newsHash] = genre_news;
        fees_for_news[newsHash] = msg.value;
        news_sender[newsHash] = msg.sender;

        // Updating the news count if applicable
        if (block.timestamp > last_time_of_updation + 24 hours) {
            uint number_of_days = (block.timestamp - last_time_of_updation) /
                (24 hours);
            if ((block.timestamp - last_time_of_updation) % (24 hours) > 0) {
                number_of_days += 1;
            }

            for (uint i = 0; i < genres.length; i++) {
                if (daily_average_news_request[genres[i]] == 0) {
                    // For the first average, use current estimate as such
                    daily_average_news_request[genres[i]] =
                        curr_news_request[genres[i]] /
                        number_of_days;
                } else {
                    // Slow moving average estimate
                    daily_average_news_request[genres[i]] =
                        ((9 * daily_average_news_request[genres[i]]) +
                            (curr_news_request[genres[i]] / number_of_days)) /
                        10;
                }
                curr_news_request[genres[i]] = 0;
            }

            last_time_of_updation = block.timestamp;
        }

        curr_news_request[genre_news] += 1;
    }

    // Function used by voters to cast vote
    // Votes registered only if voting period if active for the news
    // Note, its assumed people are calling this function with the hash of the news
    function cast_vote(bytes32 news, bool vote) external {
        if (
            news_put_time[news] != 0 &&
            news_put_time[news] + voting_period > block.timestamp
        ) {
            // Creating struct to store the name and the vote of the voter
            vote_casted memory curr_vote;
            curr_vote.voter = msg.sender;

            total_votes_casted_to_news[news] += trustworthiness[msg.sender]
                .trust_data[news_genre[news]]
                .genre_trust;

            if (vote == true) {
                curr_vote.vote = vote;
                net_votes_casted_to_news[news] += int(
                    trustworthiness[msg.sender]
                        .trust_data[news_genre[news]]
                        .genre_trust
                );
            } else {
                curr_vote.vote = vote;
                net_votes_casted_to_news[news] -= int(
                    trustworthiness[msg.sender]
                        .trust_data[news_genre[news]]
                        .genre_trust
                );
            }

            // Adding the vote details to the mapping of news storing the votes seen
            votes_casted_to_news[news].push(curr_vote);
        }
    }

    // function to help update the net correct votes required for further increase in trustworthiness
    function set_new_net_required(address voter, bytes32 genre) internal {
        // If current trustworthiness >= 51, need 10*average_news_per_day net votes
        // this helps in slow increase when already having high trustworthiness, to prevent
        // accumulation of voters with high trust scores
        if (trustworthiness[voter].trust_data[genre].genre_trust >= 51) {
            trustworthiness[voter].trust_data[genre].curr_net_required = max(
                1,
                10 * daily_average_news_request[genre]
            );
        }
        // If current trustworthiness <= 50, need 0.1*average_news_per_day net votes
        // to increase trust, to intially fastly separate honest vs non-honest
        else if (trustworthiness[voter].trust_data[genre].genre_trust <= 5) {
            trustworthiness[voter].trust_data[genre].curr_net_required = max(
                1,
                daily_average_news_request[genre] / 10
            );
        }
        // Remaining updates are in between the two extremes
        else {
            uint k = (trustworthiness[voter].trust_data[genre].genre_trust -
                1) / 5;
            trustworthiness[voter].trust_data[genre].curr_net_required = max(
                1,
                k * daily_average_news_request[genre]
            );
        }
    }

    // This function dynamically decides what is the max rating a voter can acheive based on his
    // fraction of news correctly voted. We use this policy only when rating reaches atleast 51
    function update_curr_max(address voter, bytes32 genre) internal {
        if (trustworthiness[voter].trust_data[genre].genre_trust >= 51) {
            trustworthiness[voter].trust_data[genre].max_genre_trust =
                (trustworthiness[voter].trust_data[genre].num_correct * 100) /
                (trustworthiness[voter].trust_data[genre].num_correct +
                    trustworthiness[voter].trust_data[genre].num_incorrect);

            // To prevent sudden fall of some voter who luckily reached 51 but his fraction says he should
            // be below 50, hence we set curr_max as 51 for that case so that the voter doesn't fall but
            // stays at 51
            if (trustworthiness[voter].trust_data[genre].max_genre_trust < 51) {
                trustworthiness[voter].trust_data[genre].max_genre_trust = 51;
            }
        }
    }

    function max(uint256 a, uint256 b) internal pure returns (uint256) {
        return a >= b ? a : b;
    }

    function min(uint256 a, uint256 b) internal pure returns (uint256) {
        return a <= b ? a : b;
    }

    // Internal function to update the trustworthiness of the voter
    function update_trust(
        address voter,
        bool increase,
        bytes32 genre
    ) internal {
        if (increase == true) {
            // Increasing the counts
            trustworthiness[voter].trust_data[genre].num_correct += 1;
            trustworthiness[voter].trust_data[genre].net_curr_score += 1;

            // Checking if update in trust level is possible or not
            if (
                int(
                    trustworthiness[voter].trust_data[genre].curr_net_required
                ) <= trustworthiness[voter].trust_data[genre].net_curr_score
            ) {
                trustworthiness[voter].trust_data[genre].genre_trust += 1;
                update_curr_max(voter, genre);
                trustworthiness[voter].trust_data[genre].genre_trust = min(
                    trustworthiness[voter].trust_data[genre].max_genre_trust,
                    trustworthiness[voter].trust_data[genre].genre_trust
                );

                // Getting ready for new rating level
                trustworthiness[voter].trust_data[genre].net_curr_score = 0;
                set_new_net_required(voter, genre);
            }
        } else {
            // Changing the counts appropriately
            trustworthiness[voter].trust_data[genre].num_incorrect += 1;
            trustworthiness[voter].trust_data[genre].net_curr_score -= 1;

            // Seeing if rating could potentially decrease
            if (
                -int(
                    trustworthiness[voter].trust_data[genre].curr_net_required
                ) >= trustworthiness[voter].trust_data[genre].net_curr_score
            ) {
                trustworthiness[voter].trust_data[genre].genre_trust -= 1;
                trustworthiness[voter].trust_data[genre].genre_trust = max(
                    1,
                    trustworthiness[voter].trust_data[genre].genre_trust
                );

                // Getting ready for new rating level
                trustworthiness[voter].trust_data[genre].net_curr_score = 0;
                set_new_net_required(voter, genre);
            }
        }
    }

    // Function to check if the news is real or not, note this function itself triggers the news classification
    // if news's voting period is over but no decision taken yet
    function get_status_news(bytes32 news) public payable returns (int8) {
        require(
            news_put_time[news] != 0,
            "No decision on the news was ever made on this DApp"
        );

        if (
            news_put_time[news] + voting_period <= block.timestamp &&
            is_real[news] == 0
        ) {
            // This means no decision is yet taken on the news and hence take the decision now
            if (
                total_votes_casted_to_news[news] <
                (total_votes[news_genre[news]] / 4)
            ) {
                // Means total votes casted is less than 25% hence return the money back to person who
                // put this money up for getting decision on the vote
                payable(news_sender[news]).transfer(fees_for_news[news]);
                return 0;
            }

            // Else we need to make a decision on the news
            bool news_is_real;
            if (net_votes_casted_to_news[news] >= 0) {
                is_real[news] = 1;
                news_is_real = true;
            } else {
                is_real[news] = -1;
                news_is_real = false;
            }

            // Now need to divide the benefits and update the trust
            for (uint i = 0; i < votes_casted_to_news[news].length; i++) {
                if (votes_casted_to_news[news][i].vote == news_is_real) {
                    balances[
                        votes_casted_to_news[news][i].voter
                    ] += (fees_for_news[news] /
                        total_votes_casted_to_news[news]);
                    update_trust(
                        votes_casted_to_news[news][i].voter,
                        true,
                        news_genre[news]
                    );
                } else {
                    balances[
                        votes_casted_to_news[news][i].voter
                    ] -= (fees_for_news[news] /
                        total_votes_casted_to_news[news]);
                    update_trust(
                        votes_casted_to_news[news][i].voter,
                        false,
                        news_genre[news]
                    );
                }
            }

            // Setting the balance left to 0
            fees_for_news[news] = 0;
            if (news_is_real == true) {
                return 1;
            } else {
                return -1;
            }
        }
        // Decision is already made for the news so return that
        else if (news_put_time[news] + voting_period <= block.timestamp) {
            return is_real[news];
        }
        // Decision is not yet made cause voting period is still going on
        else {
            return 0;
        }
    }

    // Function to add genre to the list of possible genre
    function add_genre(bytes32 new_genre) public payable {
        uint total_num_correct = 0;
        uint total_num_incorrect = 0;

        uint total_news_per_day = 0;

        for (uint i = 0; i < genres.length; i++) {
            require(genres[i] != new_genre, "Genre already present");

            total_num_correct += trustworthiness[msg.sender]
                .trust_data[genres[i]]
                .num_correct;
            total_num_incorrect += trustworthiness[msg.sender]
                .trust_data[genres[i]]
                .num_incorrect;
            total_news_per_day += daily_average_news_request[genres[i]];
        }
        // Fees must be paid
        require(
            msg.value >= fees_to_add_new_genre,
            "Minimum 5 eth fees should be given to add new genre"
        );

        // Must have been active for atleast large amount of time determined by the formula below
        if (
            total_num_correct - total_num_incorrect >=
            max(1000, total_news_per_day * 50)
        ) {
            payable(creator).transfer(msg.value);
            genres.push(new_genre);

            // Note we can extend this logic, by then taking a vote from all the voters who have
            // certain level of net_correct_score to decide whether or not to include a genre

            // But for now to keep things simple, we allow person giving money and having enough experience
            // to directly add the new genre
        }
    }
}
