from csv import reader 


def append_data():
    #The purpose is to load the data set and return the dataset that contains a list of transactions and further, each transaction contains several items in it.

    
    print("Hello, welcome to association rule mining\nPlease choose the dataset for which you would like to get the Association rules")
    print("Please type \n1 for Amazon\n2 for BestBuy\n3 for KMART\n4 for Nike\n5 for Custom")
    while True:
        datachoice = input()
        if (datachoice == '1'):
            data ='/Users/VINAY/midterm_datamining_vinay/amazon.csv'
            print('You selected Amazon Dataset')
            break
        elif(datachoice == '2'):
            data = '/Users/VINAY/midterm_datamining_vinay/bestbuy.csv'
            print('You selected BestBuy Dataset')
            break
        elif(datachoice == '3'):
            data = '/Users/VINAY/midterm_datamining_vinay/kmart.csv'
            print('You selected KMART Dataset')
            break
        elif(datachoice == '4'):
            data = '/Users/VINAY/midterm_datamining_vinay/nike.csv'
            print('You selected Nike Dataset')
            break
        elif(datachoice == '5'):
            data = '/Users/VINAY/midterm_datamining_vinay/grocery.csv'
            print('You selected Custom Dataset')
            break
        else:
            print("Please select a valid choice from the above list")
    with open(data, 'r',encoding="windows-1252") as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)

        # Pass reader object to list() to get a list of lists
        dataset = list(csv_reader)
        for items in dataset:
            for j in range(0, len(items)):
                for items1 in items:

                    if items1 == "":
                        items.remove("")

    return dataset

def gen_Candidate1(dataset):
    # Generate and return a set(dataset) which contains all frequent candidate 1-itemsets.

    Can1 = set()
    for t in dataset:
        for item in t:
            item_set = frozenset([item])
            Can1.add(item_set)
    return Can1


def apriori(Cank_item, Lisk1):
    #To check whether a frequent candidate k-itemset satisfy Apriori property and return true/false accordingly.


    for item in Cank_item:
        sub_Cank = Cank_item - frozenset([item])
        if sub_Cank not in Lisk1:
            return False
    return True


def gen_Cank(Lisk1, k):
    #Generate and return candidate k, a set which contains all frequent candidate k-itemsets.

    Cank = set()
    length_Lisk1 = len(Lisk1)
    listof_Lisk1 = list(Lisk1)
    for i in range(length_Lisk1):
        for j in range(1, length_Lisk1):
            list1 = list(listof_Lisk1[i])
            list2 = list(listof_Lisk1[j])
            list1.sort()
            list2.sort()
            if list1[0:k-2] == list2[0:k-2]:
                Cank_item = listof_Lisk1[i] | listof_Lisk1[j]
                if apriori(Cank_item, Lisk1):
                    Cank.add(Cank_item)
    return Cank


def gen_Lisk(dataset, Cank, minsup, sup_data):
    #Generate and return a list/set which contains all frequent k-itemsets.

    Lisk = set()
    item_count = {}
    for t in dataset:
        for item in Cank:
            if item.issubset(t):
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1
    t_num = float(len(dataset))
    for item in item_count:
        if (item_count[item] / t_num) >= minsup:
            Lisk.add(item)
            sup_data[item] = item_count[item] / t_num
    return Lisk


def gen_L(dataset, k, minsup):
    #Generate all frequent itemsets by the value of minimum support’s input.

    sup_data = {}
    Can1 = gen_Candidate1(dataset)
    List1 = gen_Lisk(dataset, Can1, minsup, sup_data)
    Lisksub1 = List1.copy()
    List = []
    List.append(Lisksub1)
    for i in range(2, k+1):
        Ci = gen_Cank(Lisksub1, i)
        Li = gen_Lisk(dataset, Ci, minsup, sup_data)
        Lisksub1 = Li.copy()
        List.append(Lisksub1)
    return List, sup_data


def association_rules(List, sup_data, minconf):
    #Generate and return association rules.

    asso_rules = []
    sublist = []
    for i in range(0, len(List)):
        for freq_set in List[i]:
            for sub_set in sublist:
                if sub_set.issubset(freq_set):
                    conf = sup_data[freq_set] / sup_data[freq_set - sub_set]
                    rule = (freq_set - sub_set, sub_set, conf)
                    if conf >= minconf and rule not in asso_rules:
                        # print freq_set-sub_set, " => ", sub_set, "conf: ", conf
                        asso_rules.append(rule)
            sublist.append(freq_set)
    return asso_rules


if __name__ == "__main__":

    #print("Please enter the min_support")
    #inp = input("Enter the minimum support: ")

    dataset = append_data()
    List, sup_data = gen_L(dataset, k=3, minsup = float(input("Enter the minimum support: ")))
    rules_list = association_rules(List, sup_data, minconf= float(input("Enter the minimum Confidence: ")))
    for Lisk in List:
        print("-*"*40)
        print("frequent " + str(len(list(Lisk)[0])) + "-itemsets\t\tsupport")
        print("-*"*40)
        for freq_set in Lisk:
            print(freq_set, sup_data[freq_set])
    print("\n")
    print("#-"*40)
    print("Association Rules with Confidence")
    print("#-"*40)
    for item in rules_list:
        print(item[0], "=>", item[1], "confidence: ", item[2])
